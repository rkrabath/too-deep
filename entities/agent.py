#!/usr/bin/python

import sys
import pygame
import multiprocessing
import networkx as nx
from pygame.locals import *

from point import Point

class Agent(object):
    def __init__(self, initial_location, dispatch):
        self.location = initial_location 
        self.dispatch = dispatch

        self.parent_end, child_end = multiprocessing.Pipe()

        self.process = multiprocessing.Process(target=self.main_loop, args=(child_end, ))
        self.process.start()

        self.parent_end.send({'command': 'update_map', 'payload': self.dispatch.map.graph})

        items_payload = [
                {
                    'category': x.category,
                    'name': x.name,
                    'location': x.location,
                } for x in self.dispatch.items 
            ]
        self.parent_end.send({'command': 'update_items', 'payload': items_payload})

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
                self.parent_end.send({'command': 'die'})
                self.cleanup()
                self.alive = False


    def inform_of_new_item(self, new_item):
        item_payload = {
                    'category': new_item.category,
                    'name': new_item.name,
                    'location': new_item.location,
                } 
        self.parent_end.send({'command': 'new_item', 'payload': item_payload})


############ Below here is the child process ############################

    def main_loop(self, parent):

        self.dispatch = None # It's in a different process now...

        self.parent = parent

        # Initialize some variables in the child
        self.map = None
        self.items = []
        self.route = None

        self.goals = [
            'exit',
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
            
            if message['command'] == 'update_items':
                self.items = message['payload']

            if message['command'] == 'new_item':
                self.items.append(message['payload'])



    def greatest_desire(self):
        return 'food'
        return 'work'
        return 'wander'

        
    def act(self):
        if not self.route:
            print('no route found')
            goal = self.greatest_desire()
            target_location = self.get_location_of_category(goal)
            print self.location, target_location
            print type(self.location), type(target_location)
            if target_location != self.location:
                print("computing new route")
                self.route = self.pathfind_to(target_location)


        self.follow_route()

        if not self.still_alive():
            self.parent.send({'command': 'kill_me'})


    def get_location_of_category(self, category):
        for item in self.items:
            print item
            if item['category'] == category:
                return item['location']

    def still_alive(self):
        if Point(100,50,50) == self.location:
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
            self._move_to(next_location)
        else:
            print "NO ROUTE DEFINED"
                

    def _move_to(self, destination):
        # TODO: add some verification here to ensure we don't move through walls
        self.location = destination
        self.parent.send({'command': 'new_position', 'payload': destination})
