#!/usr/bin/python

import sys
import time
import pygame
import networkx as nx
from pygame.locals import *

import entities as e


min = 0
max = 32
scale = 32

map = e.Map(max)
dispatch = e.Dispatch(map)
display = e.Display(map, dispatch, scale)
input = e.Input(display, dispatch)
            
#map.print_grid()
print "================================="



# run the game loop
last_time = 0.0
while True:
    current_time = time.time()
    input.process()
    display.update()
    time.sleep(0.2)
    if current_time > last_time + 1:
        dispatch.update()
        last_time = current_time


