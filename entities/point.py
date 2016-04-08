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
        if self.z == other.z:
            if self.x == other.x:
                if self.y == other.y:
                    return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return int("{0:03d}{1:03d}{2:03d}".format(self.z, self.x, self.y))

    def xy(self):
        return (self.x, self.y)

    def xy_display(self, scale):
        return (self.x * scale, self.y * scale )

