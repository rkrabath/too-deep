#!/usr/bin/python

import sys
import pygame
import multiprocessing
import networkx as nx
from pygame.locals import *

from agent import Agent
from item import Item
from point import Point

class Dispatch(object):
    def __init__(self, map):
        self.agents = []
        self.items = []
        self.map = map
        
        self.iterator = self.auto_increment()

        middle = map.max/2
        self.create_item_at(Point(map.max, 2, 2))
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
    

    def create_item_at(self, location):
        item = Item('food', 'meat', location)
        self.items.append(item)
        
        for agent in self.agents:
            agent.inform_of_new_item(item)

    
    def exit(self):
        for agent in self.agents:
            agent.exit()


