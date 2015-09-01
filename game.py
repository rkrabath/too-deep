#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

import entities as e


min = 0
max = 10
scale = 100

map = e.Map(max)
display = e.Display(map, scale)
input = e.Input(display)
            
#map.print_grid()
print "================================="



# run the game loop
while True:
    input.process()
    display.update()


