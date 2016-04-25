#!/usr/bin/python

import sys
import pygame
import multiprocessing
import networkx as nx
from pygame.locals import *

from point import Point

class Agent(object):
    def __init__(self, dispatch_pipe, initial_location):
        self.dispatch_pipe = dispatch_pipe
        self.location = initial_location 
        self.map = None
        self.route = None
        self.alive = True

        self.goals = [
            'exit',
            'food',
            'drink',
        ]

        self.process = multiprocessing.Process(target=self.main_loop)
        self.process.start()


    def cleanup(self):      # Must call this when agent finishes.
        self.process.join()     

    
    def main_loop(self):
        while True:
            message = self.dispatch_pipe.recv()

            if message['command'] == "tick":
                self.act()

            if message['command'] == "die":
                return

            if message['command'] == 'update_map':
                self.map = message['payload']

            


    def greatest_desire(self):
        return 'exit'

        
    def act(self):
        #if not self.route:
        #    print('no route found')
        #    goal = self.greatest_desire()
        #    target_location = self.dispatch.find(goal)
        #    print self.location, target_location
        #    print type(self.location), type(target_location)
        #    if target_location != self.location:
        #        print("computing new route")
        #        self.route = self.pathfind_to(target_location)

        # === LOAD TESTING ===
        goal = self.greatest_desire()
        # TODO: ask dispatch for destination point
        #target_location = self.dispatch.find(goal)
        self.route = self.pathfind_to(Point(100,50,50))

        self.follow_route()

        self.check_still_alive()


    def check_still_alive(self ):
        if Point(100,50,50) == self.location:
            self.dispatch_pipe.send({'command': 'kill_me'})


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
        self.dispatch_pipe.send({'command': 'new_position', 'payload': destination})
