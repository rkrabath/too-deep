#!/usr/bin/python

import sys
import yaml
import pygame
import multiprocessing
import networkx as nx
from pygame.locals import *

from point import Point

class Item(object):
    def __init__(self, path, initial_location):
        self.location = initial_location 

        tokens = path.split('/')
        file_name = tokens[0] + '.yaml'
        data_structure_path = tokens[1:]
        with open('data/items/'+file_name, 'r') as f:
            all_items = yaml.load(f.read())

        item = all_items
        for child in data_structure_path:
            item = item[child]
        self.name = tokens[-1]
        self.category = tokens[-2]
        self.capabilities = item['capabilities']
        self.sprite = pygame.Rect(*[int(i) for i in item['sprite'].split(',')])
    


