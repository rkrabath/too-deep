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
        self.create_exit_at(Point(max, middle, middle))


    def create_agent_at(self, location):
        self.agents.append(Agent(location))
    

    def create_exit_at(self, location):
        if self.exit:
            raise ValueError('The exit was already placed.')
        self.exit = location

