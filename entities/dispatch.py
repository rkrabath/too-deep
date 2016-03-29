#!/usr/bin/python

import sys
import pygame
import networkx as nx
from pygame.locals import *

from agent import Agent

class Dispatch(object):
    def __init__(self, map):
        self.agents = []
        self.map = map

    def create_agent_at(self, location):
        self.agents.append(Agent(location))
 

