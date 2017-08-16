#!/usr/bin/python

import sys
import copy
import networkx as nx
import pygame
from pygame.locals import *

import map as game_map
from point import Point
from pointset import Pointset


class Mode(object):
    def __init__(self):
	self.options = [ 'DIG' ]
        self.current = None

    def switch(self, new_mode):
        if new_mode in self.options:
            self.current = new_mode
        else:
            raise ValueError("Invalid mode: " + new_mode)

    def exit(self):
        self.current = None


        

class Input(object):
    def __init__(self, display, dispatch):
        self.display = display
        self.dispatch = dispatch
        self.cursor = [5,5]
        self.selected = None
        self.selections = Pointset()
        self.shift_down = False
        self.ctrl_down = False
        self.alt_down = False

        self.down_options = {
                    32 : self.select, # ' '
                    44 : self.display.level_up, # '<'
                    46 : self.display.level_down, # '>'
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
                    #print "Key pressed with no action defined: ", event
                    pass
            elif event.type == KEYUP:
                try:
                    self.up_options[event.key]()
                except KeyError:
                    #print "Key released with no action defined: ", event
                    pass
            elif event.type == MOUSEMOTION:
                node = list(self.display.get_coord(event.pos).xy())
                self.cursor = node
                self.update_selection()
            elif event.type == MOUSEBUTTONDOWN:
                node = self.display.get_coord(event.pos)
                if event.button == 1:
                   # if game_map.is_traversable(node):
                   #     game_map.make_not_traversable(node)
                   # else:
                   #     game_map.make_traversable(node)
                    self.select()
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
        self.update_selection()

    def down(self):
        self.cursor[1] += 1    
        self.update_selection()

    def left(self):
        self.cursor[0] -= 1    
        self.update_selection()

    def right(self):
        self.cursor[0] += 1    
        self.update_selection()

    def update_selection(self):
        self.display.highlight_node(self.cursor)
        if self.selected:
            end_point = copy.copy(self.cursor)
            normalized = self.normalize_box((self.selected, end_point))
            self.display.highlight_selecting(normalized)
     
    def select(self):
        if self.selected:
            end_point = copy.copy(self.cursor)
            a,b = self.normalize_box((self.selected, end_point))
            all_points = self.points_in_box(a,b)
            self.selections = self.selections + all_points
            self.display.highlight_selecting(None)
            self.display.highlight_selections(self.selections)
            self.selected = None
        else:
            self.selected = copy.copy(self.cursor)

    def points_in_box(self, point_a, point_b):
        """ Return a set of points that are in a rectangle defined by a and b """
        points = []
        for x in xrange(point_a[0], point_b[0]+1):
            for y in xrange(point_a[1], point_b[1]+1):
                points.append(Point(0,x,y))
        pointss = Pointset(points)
        return pointss

    def normalize_box(self, box):
        """ Given a set of coordinates ((x,y),(x,y)), return the top left and bottom right points """
        try:
            a, b = box
        except ValueError:
            sys.exit("Passed something that wasn't ((x,y),(x,y)) to normalize_box()")

        # a--+
        # |  |
        # |  |
        # +--b

        if a[0] <= b[0] and a[1] <= b[1]:
            # happy path, no changes necessary
            return box 

        # b--+
        # |  |
        # |  |
        # +--a   

        if a[0] >= b[0] and a[1] >= b[1]:
            # They're reversed.  Swap them.
            return (b,a)  
         
        # +--a
        # |  |
        # |  |
        # b--+

        # OR

        # +--b
        # |  |
        # |  |
        # a--+

        # Need to compute the opposite corners
        c = (a[0],b[1])
        d = (b[0],a[1])
        return self.normalize_box((c,d)) # We computed new corners, 
        #then we call back to make sure they're in the right order.




