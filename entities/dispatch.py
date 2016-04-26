#!/usr/bin/python

import sys
import pygame
import multiprocessing
import networkx as nx
from pygame.locals import *

from agent import Agent
from point import Point

class Dispatch(object):
    def __init__(self, map):
        self.agents = []
        self.exit = None
        self.map = map
        
        self.iterator = self.auto_increment()

        middle = map.max/2
        self.create_exit_at(Point(map.max, middle, middle))
        print Point(map.max, middle, middle)


    
    def auto_increment(self):
        next_value = 0
        while True:
            yield next_value
            next_value += 1


    def update(self):
        self.agents = [agent for agent in self.agents if agent.alive]

        for agent in self.agents:
            agent.tick()
      

    def create_agent_at(self, location):
        agent = Agent(location, self)
        self.agents.append(agent)
    

    def create_exit_at(self, location):
        if self.exit:
            raise ValueError('The exit was already placed.')
        self.exit = location


    def find(self, thing):
        if thing == 'exit':
            return self.exit
