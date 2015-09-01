#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

class Input(object):
    def __init__(self, display):
        self.display = display
        self.shift_down = False
        self.ctrl_down = False
        self.alt_down = False

        self.down_options = {
                    '>' : self.display.level_down,
                    '<' : self.display.level_up,
                }

        self.up_options = {
                }

        self.ignored_input_types = [ ACTIVEEVENT, MOUSEBUTTONUP, KEYUP]

    def exit(self):
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
                    self.down_options[event.unicode]()
                except KeyError:
                    print "Key pressed with no action defined: ", event.key, "|"+event.unicode+"|", event.mod
            elif event.type == MOUSEMOTION:
                node = self.display.get_coord(event.pos)
                self.display.highlight_node(node)
            elif event.type == MOUSEBUTTONDOWN:
                node = self.display.get_coord(event.pos)
                print "Clicked on " + ", ".join([str(x) for x in node.xy()])
                if self.display.map.is_traversable(node):
                    self.display.map.make_not_traversable(node)
                else:
                    self.display.map.make_traversable(node)
            else:
                print "Unrecongized entry: ", event.type
    
