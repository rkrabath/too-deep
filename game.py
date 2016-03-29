#!/usr/bin/python

import sys
import time
import pygame
import networkx as nx
from pygame.locals import *

import entities as e


min = 0
max = 10
scale = 100

map = e.Map(max)
dispatch = e.Dispatch(map)
display = e.Display(map, dispatch, scale)
input = e.Input(display, dispatch)
            
#map.print_grid()
print "================================="



# run the game loop
while True:
    input.process()
    display.update()
    time.sleep(1)


