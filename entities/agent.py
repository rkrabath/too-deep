#!/usr/bin/python

import sys
import pygame
import random
import multiprocessing
import networkx as nx
from pygame.locals import *

from point import Point
import map as game_map

class Agent(object):
    def __init__(self, initial_location, dispatch):
        self.location = initial_location 
        self.dispatch = dispatch

        self.parent_end, child_end = multiprocessing.Pipe()

        self.process = multiprocessing.Process(target=self.main_loop, args=(child_end, dispatch.items))
        self.process.start()

        self.parent_end.send({'command': 'update_map', 'payload': game_map.graph})

        self.alive = True


    def cleanup(self):      # Must call this when agent finishes.
        self.process.join()     

    
    def tick(self):
        # TODO: Need to send a map update periodically, but how to know when to do it?
        self.parent_end.send({'command': 'tick'})        
        while self.parent_end.poll():
            message = self.parent_end.recv()
            if message['command'] == 'new_position':
                self.location = message['payload']
            if message['command'] == 'kill_me':
                self.exit()


    def exit(self):
        self.parent_end.send({'command': 'die'})
        self.cleanup()
        self.alive = False
        

############ Below here is the child process ############################

    def main_loop(self, parent, items):

        self.dispatch = None # It's in a different process now...

        self.parent = parent

        # Initialize some variables in the child
        self.map = None
        self.items = items # self.items is a proxy object: https://docs.python.org/2/library/multiprocessing.html#proxy-objects
        self.route = None

        self.hunger_percent = 70 
        self.thirst_percent = 20
        self.tired_percent = 0

        self.goals = [
            'food',
            'drink',
        ]

        # Main loop.  When this exits the process will end.
        while True:
            message = self.parent.recv()

            if message['command'] == "tick":
                self.act()

            if message['command'] == "die":
                return

            if message['command'] == 'update_map':
                self.map = message['payload']

            if message['command'] == 'new_item':
                self.items.append(message['payload'])


    def greatest_desire(self):
        if self.hunger_percent > 75:
            return 'food'
        if self.thirst_percent > 75:
            return 'drink'
        # return 'work'
	return None

        
    def act(self):
        if self.hunger_percent > 75 and 'food' in self.items_at_location(self.location): # This probably doesn't work
            hunger_percent = 0
        if self.thirst_percent > 75 and 'drink' in self.items_at_location(self.location): # This probably doesn't work
            thirst_percent = 0
        if not self.route:
            goal = self.greatest_desire()
            target_location = self.get_location_of_category(goal)
            if target_location != self.location:
                self.route = self.pathfind_to(target_location)

        self.follow_route()

        if not self.still_alive():
            self.parent.send({'command': 'kill_me'})

    
    def items_at_location(self, location):
        return [item for item in self.items if item.location == location]


    def get_location_of_category(self, category):
        for item in self.items:
            if item.category == category:
                return item.location


    def still_alive(self):
        if self.hunger_percent > 105: 
            print('Died of hunger!')
            return False
        elif self.thirst_percent > 105:
            print('Died of thirst!')
            return False
        else:
            return True


    def pathfind_to(self, target_location):
        try:
            return nx.astar_path(self.map, self.location, target_location)[1:]
        except nx.exception.NetworkXNoPath:
            return None
            

    def follow_route(self):
        if self.route:
            next_location = self.route.pop(0)
        else:
            next_location = random.choice(list(nx.all_neighbors(self.map, self.location)))
        self._move_to(next_location)
                

    def _move_to(self, destination):
        # TODO: add some verification here to ensure we don't move through walls
        self.location = destination
        self.parent.send({'command': 'new_position', 'payload': destination})
        self.hunger_percent += 1
        self.thirst_percent += 1
