#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

class Point(object):
    def __init__(self,z,x,y):
        if z < 0 or x < 0 or y < 0:
            raise ValueError("Values less than 0 are not allowed")
        self.z = z
        self.x = x
        self.y = y

    def __repr__(self):
        return "({0},{1},{2})".format(self.z, self.x, self.y)

    def __eq__(self, other):
        try:
            if self.z == other.z:
                if self.x == other.x:
                    if self.y == other.y:
                        return True
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return int("{0:03d}{1:03d}{2:03d}".format(self.z, self.x, self.y))

    def xy(self):
        return (self.x, self.y)

    def left_neighbor(self):
        try:
            return Point(self.z, self.x-1, self.y)
        except ValueError:
            return None

    def right_neighbor(self):
        try:
            return Point(self.z, self.x+1, self.y)
        except ValueError:
            return None

    def top_neighbor(self):
        try:
            return Point(self.z, self.x, self.y-1)
        except ValueError:
            return None

    def bottom_neighbor(self):
        try:
            return Point(self.z, self.x, self.y+1)
        except ValueError:
            return None

    def xy_display(self, scale):
        return (self.x * scale, self.y * scale )

    def xy_display_offset(self, scale):
        return (self.x * scale - scale / 2, self.y * scale - scale / 2)

