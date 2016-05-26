#!/usr/bin/env python

import sys
import time
import pygame
import networkx as nx
from pygame.locals import *

import entities as e


min = 0
max = 32
scale = 32

game_map = e.map
game_map.init(32)
dispatch = e.Dispatch()
display = e.Display(scale)
input = e.Input(display, dispatch)
            
print "================================="



# run the game loop
last_time = 0.0
while True:
    current_time = time.time()
    input.process()
    display.update(dispatch.agents, dispatch.items)
    time.sleep(0.2)
    if current_time > last_time + 1:
        dispatch.update()
        last_time = current_time


