#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

from point import Point

class Display(object):

    def __init__(self, map, dispatch, scale):
        # set up the colors
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.RED   = (255,   0,   0)
        self.GREEN = (  0, 255,   0)
        self.BLUE  = (  0,   0, 255)
        pygame.init()
        self.map = map
        self.dispatch = dispatch
        self.scale = scale
        self.layer = self.map.max
        self.highlighted_coordinate = None
    
        dimension = self.scale * self.map.max + 2
        self.DISPLAYSURF = pygame.display.set_mode((dimension, dimension), pygame.SRCALPHA, 32)

        # set up the window
        pygame.display.set_caption('Drawing')


    def level_down(self):
        if not self.layer - 1 < self.map.min:
            self.layer -= 1
        print "Displaying layer " + str(self.layer)

        
    def level_up(self):
        if not self.layer + 1 > self.map.max:
            self.layer += 1
        print "Displaying layer " + str(self.layer)


    def get_coord(self, point):
        """ Translate display points to map points """
        offset = self.scale/2
        # offset, round considerably (integer division)
        
        protopoint = [(sub+offset)/self.scale for sub in point]
        return Point(self.layer, *protopoint)
        

    def draw_agents(self):
        for agent in self.dispatch.agents:
            x, y = agent.location.xy()
            pygame.draw.circle(self.DISPLAYSURF, self.BLUE, (x*self.scale, y*self.scale-self.scale/4), self.scale/8, self.scale/25)
            pygame.draw.line(self.DISPLAYSURF, self.BLUE, (x*self.scale, y*self.scale-self.scale/8),(x*self.scale, y*self.scale+self.scale/8), self.scale/25)
            pygame.draw.line(self.DISPLAYSURF, self.BLUE, (x*self.scale, y*self.scale),(x*self.scale+self.scale/8, y*self.scale-self.scale/8), self.scale/25)
            pygame.draw.line(self.DISPLAYSURF, self.BLUE, (x*self.scale, y*self.scale),(x*self.scale-self.scale/8, y*self.scale-self.scale/8), self.scale/25)
            pygame.draw.line(self.DISPLAYSURF, self.BLUE, (x*self.scale, y*self.scale+self.scale/8),(x*self.scale+self.scale/8, y*self.scale+self.scale/4), self.scale/25)
            pygame.draw.line(self.DISPLAYSURF, self.BLUE, (x*self.scale, y*self.scale+self.scale/8),(x*self.scale-self.scale/8, y*self.scale+self.scale/4), self.scale/25)

    
    def draw_exit(self):
        if self.dispatch.exit:
            x,y = self.dispatch.exit.xy()
            pygame.draw.rect(self.DISPLAYSURF, self.BLACK, pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale), self.scale/20)


    def highlight_node(self, point):
        self.highlighted_coordinate = point


    def show_highlight(self):
        if self.highlighted_coordinate:
            display_point = [(x*self.scale-self.scale/2) for x in self.highlighted_coordinate.xy()]
            s = pygame.Surface((self.scale,self.scale))
            s.set_alpha(128)
            s.fill(self.RED)
            self.DISPLAYSURF.blit(s, display_point)


    def update(self):
        # draw on the surface object
        self.DISPLAYSURF.fill(self.WHITE)

        for node in nx.nodes(self.map.graph):
            if node.z != self.layer:
                continue
            pygame.draw.circle(self.DISPLAYSURF, self.BLUE, node.xy_display(self.scale), self.scale/5, 0)

        for edge in nx.edges(self.map.graph):
            if node.z != self.layer:
                continue
            pygame.draw.line(self.DISPLAYSURF, self.GREEN, edge[0].xy_display(self.scale), edge[1].xy_display(self.scale), self.scale/50) 

        self.draw_agents()

        self.draw_exit()

        self.show_highlight()
    
        pygame.display.update()

