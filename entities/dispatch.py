#!/usr/bin/python

import os
import sys
import yaml
import pygame
import multiprocessing
import networkx as nx
from pygame.locals import *

from agent import Agent
from item import Item
from point import Point

class Dispatch(object):
    def __init__(self, map):
        self.map = map
        self.agents = []
        self.state_manager = multiprocessing.Manager()
        self.items = self.state_manager.list()

        self.create_item_at('food/meat/shank', Point(map.max, 2, 2))
        self.create_item_at('food/meat/bacon', Point(map.max, 2, 3))
        self.create_item_at('food/meat/steak', Point(map.max, 2, 4))


    def update(self):
        self.agents = [agent for agent in self.agents if agent.alive]

        for agent in self.agents:
            agent.tick()
      

    def create_agent_at(self, location):
        agent = Agent(location, self)
        self.agents.append(agent)
    

    def create_item_at(self, item_type, location):
        item = Item(item_type, location)
        self.items.append(item)

    
    def exit(self):
        for agent in self.agents:
            agent.exit()


