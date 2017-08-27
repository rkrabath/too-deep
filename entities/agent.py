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
    def __init__(self, initial_location, dispatch, hunger_percent=0, thirst_percent=0):
        self.location = initial_location 
        self.dispatch = dispatch

        self.parent_end, child_end = multiprocessing.Pipe()

        self.process = multiprocessing.Process(target=self.main_loop, args=(child_end, dispatch.items, hunger_percent, thirst_percent))
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
            if message['command'] == 'get_order':
                self.parent_end.send({'command': 'new_order',
                                      'payload': self.dispatch.first_order()})

    def exit(self):
        self.parent_end.send({'command': 'die'})
        self.cleanup()
        self.alive = False
        

############ Below here is the child process ############################

    def main_loop(self, parent, items, hunger_percent, thirst_percent):

        self.dispatch = None # It's in a different process now...

        self.parent = parent

        # Initialize some variables in the child
        self.map = None
        self.items = items # self.items is a proxy object: https://docs.python.org/2/library/multiprocessing.html#proxy-objects
        self.route = None

        self.hunger_percent = hunger_percent
        self.thirst_percent = thirst_percent
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


    def greatest_desire(self):
        if self.hunger_percent > 75:
            return 'satiate'
        if self.thirst_percent > 75:
            return 'intoxicate'

        
    def act(self):
        if self.hunger_percent > 75 and self.capability_at_location('satiate'): 
            self.hunger_percent = 0
        if self.thirst_percent > 75 and self.capability_at_location('intoxicate'): 
            self.thirst_percent = 0

        if not self.route:
            goal = self.greatest_desire()

            if goal: 
                target_location = self.location_of_capability(goal)
            else:
                target_location = self.get_order()

            print target_location
            print self.location

            if target_location != self.location:
                self.route = self.pathfind_to(target_location)

        self.follow_route()

        if not self.still_alive():
            self.parent.send({'command': 'kill_me'})

    
    def items_at_location(self, location):
        return [item[0] for item in self.items if item[1] == location]


    def capability_at_location(self, capability):
        for item in self.items_at_location(self.location):
            if capability in item.capabilities:
                return True
        return False

    
    def location_of_capability(self, capability):
        for item in self.items:
            if capability in item[0].capabilities:
                return item[1]

    
    def get_order(self):
        self.parent.send({'command': 'get_order'})

        while True:
            print 'waiting on order'
            self.parent_end.poll(5)

            message = self.parent.recv()
            print message
            if message['command'] == 'new_order':
                # Just ignore ticks while waiting for order
                return message['payload']


    def still_alive(self):
        if self.hunger_percent > 105: 
            return False
        elif self.thirst_percent > 105:
            return False
        else:
            return True


    def pathfind_to(self, target_location):
        print nx.astar_path(self.map, self.location, target_location)[1:]

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
