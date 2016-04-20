#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

class Agent(object):
    def __init__(self, dispatch, initial_location):
        self.dispatch = dispatch
        self.location = initial_location 
        self.route = None
        self.alive = True

        self.goals = [
            'exit',
            'food',
            'drink',
        ]

    def greatest_desire(self):
        return 'exit'

        
    def act(self):
        if not self.route:
            print('no route found')
            goal = self.greatest_desire()
            target_location = self.dispatch.find(goal)
            print self.location, target_location
            print type(self.location), type(target_location)
            if target_location != self.location:
                print("computing new route")
                self.route = self.pathfind_to(target_location)

        print self, self.route
        self.follow_route()

        self.check_still_alive()


    def check_still_alive(self ):
        if self.dispatch.find('exit') == self.location:
            self.alive = False


    def pathfind_to(self, target_location):
        try:
            return nx.astar_path(self.dispatch.map.graph, self.location, target_location)[1:]
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
