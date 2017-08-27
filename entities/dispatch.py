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
    def __init__(self):
        self.agents = []
        self.state_manager = multiprocessing.Manager()
        self.items = self.state_manager.list()
        self.orders = {
            'ditch': [],
            'stairs': [],
            'tunnel': [],
            'ramp': [],
        }


    def update(self):
        self.agents = [agent for agent in self.agents if agent.alive]

        for agent in self.agents:
            agent.tick()

    def first_order(self):
        for order, location_list in self.orders.iteritems():
            if location_list:
                return location_list.pop()
      

    def create_agent_at(self, location):
        agent = Agent(location, self)
        self.agents.append(agent)
    

    def create_item_at(self, item_type, location):
        item = Item(item_type)
        self.items.append((item, location))

    
    def exit(self):
        for agent in self.agents:
            agent.exit()
