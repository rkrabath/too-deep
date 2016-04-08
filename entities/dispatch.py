#!/usr/bin/python

import sys
import pygame
import networkx as nx
from pygame.locals import *

from agent import Agent
from point import Point

class Dispatch(object):
    def __init__(self, map):
        self.agents = []
        self.exit = None
        self.map = map

        middle = map.max/2
        self.create_exit_at(Point(map.max, middle, middle))

    
    def update(self):
        self.agents = [agent for agent in self.agents if agent.alive]
        for agent in self.agents:
            agent.act()
      


    def create_agent_at(self, location):
        self.agents.append(Agent(self, location))
    

    def create_exit_at(self, location):
        if self.exit:
            raise ValueError('The exit was already placed.')
        self.exit = location


    def find(self, thing):
        if thing == 'exit':
            return self.exit
