#!/usr/bin/python

import sys
import pygame
import multiprocessing
import networkx as nx
from pygame.locals import *

from point import Point

class Item(object):
    def __init__(self, category, name, initial_location):
        self.location = initial_location 
        self.category = category
        self.name = name


