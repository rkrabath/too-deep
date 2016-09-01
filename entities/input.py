#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

import map as game_map

class Input(object):
    def __init__(self, display, dispatch):
        self.display = display
        self.dispatch = dispatch
        self.cursor = [5,5]
        self.selected = []
        self.shift_down = False
        self.ctrl_down = False
        self.alt_down = False

        self.down_options = {
                    44 : self.display.level_up, # <
                    46 : self.display.level_down, # >
                   303 : self.shift_pressed,
                   304 : self.shift_pressed,
                   305 : self.ctrl_pressed,
                   306 : self.ctrl_pressed,
                   307 : self.alt_pressed,
                   308 : self.alt_pressed,
                   273 : self.up,
                   274 : self.down,
                   275 : self.right,
                   276 : self.left,
	
                }


        self.up_options = {
                   303 : self.shift_released,
                   304 : self.shift_released,
                   305 : self.ctrl_released,
                   306 : self.ctrl_released,
                   307 : self.alt_released,
                   308 : self.alt_released,
                }

        self.ignored_input_types = [ ACTIVEEVENT, MOUSEBUTTONUP]

        self.display.highlight_node(self.cursor)

    def exit(self):
        self.dispatch.exit()
        pygame.quit()
        sys.exit()
        

    def process(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type in self.ignored_input_types:
                continue
            elif event.type == QUIT:
                self.exit()
            elif event.type == KEYDOWN:
                try:
                    self.down_options[event.key]()
                except KeyError:
                    print "Key pressed with no action defined: ", event
            elif event.type == KEYUP:
                try:
                    self.up_options[event.key]()
                except KeyError:
                    print "Key released with no action defined: ", event
            elif event.type == MOUSEMOTION:
                node = self.display.get_coord(event.pos)
                self.display.highlight_node(node.xy())
            elif event.type == MOUSEBUTTONDOWN:
                node = self.display.get_coord(event.pos)
                if event.button == 1:
                    if game_map.is_traversable(node):
                        game_map.make_not_traversable(node)
                    else:
                        game_map.make_traversable(node)
                elif event.button == 3:
                    self.dispatch.create_agent_at(node)
            else:
                print "Unrecongized entry: ", event.type
    
    def shift_pressed(self):
        self.shift_down = True

    def shift_released(self):
        self.shift_down = False

    def ctrl_pressed(self):
        self.ctrl_down = True

    def ctrl_released(self):
        self.ctrl_down = False

    def alt_pressed(self):
        self.alt_down = True

    def alt_released(self):
        self.alt_down = False

    def up(self):
        self.cursor[1] -= 1    
        self.display.highlight_node(self.cursor)

    def down(self):
        self.cursor[1] += 1    
        self.display.highlight_node(self.cursor)

    def left(self):
        self.cursor[0] -= 1    
        self.display.highlight_node(self.cursor)

    def right(self):
        self.cursor[0] += 1    
        self.display.highlight_node(self.cursor)

