#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

class Agent(object):
    def __init__(self, initial_location):
        self.location = initial_location 


