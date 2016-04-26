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


############ Below here is the child process ############################

    def main_loop(self, parent):

        self.dispatch = None # It's in a different process now...

        self.parent = parent

        # Initialize some variables in the child
        self.map = None
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

        if not self.still_alive():
            self.parent.send({'command': 'kill_me'})


    def still_alive(self ):
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
