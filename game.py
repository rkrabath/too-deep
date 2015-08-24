#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

class Point(object):
    def __init__(self,z,x,y):
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

    def __hash__(self):
        return int("{0:03d}{1:03d}{2:03d}".format(self.z, self.x, self.y))

    def xy(self):
        return (self.x, self.y)

    def xy_display(self, scale):
        return (self.x * scale, self.y * scale)


class Map(object):
    def __init__(self,dimension):
        self.graph = nx.Graph()
        self.min = 0
        self.max = dimension+1

        # Create nodes for topmost layer:
        for x in range(self.min,self.max):
            for y in range(self.min,self.max):
                # add node:
                p = Point(dimension,x,y)
                self.graph.add_node(p)

        for x in range(self.min,self.max):
            for y in range(self.min,self.max):
                p = Point(self.max,x,y)
                # connect node:
                # compute neighbors:
                south_point = Point(dimension,x,y-1)
                west_point = Point(dimension,x-1,y)
                
                if x != min:
                    self.graph.add_edge(p,west_point)
                if y != min:
                    self.graph.add_edge(p,south_point)
                
    def print_grid(self):
        for node in nx.nodes(self.graph):
            print node
            for neighbor in nx.all_neighbors(self.graph, node):
                print " " + str(neighbor)

        
class Display(object):

    def __init__(self, map, scale):
        # set up the colors
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.RED   = (255,   0,   0)
        self.GREEN = (  0, 255,   0)
        self.BLUE  = (  0,   0, 255)
        pygame.init()
        self.map = map
        self.scale = scale
        self.layer = self.map.max
    
        dimension = self.scale * self.map.max + 2
        self.DISPLAYSURF = pygame.display.set_mode((dimension, dimension), 0, 32)

        # set up the window
        pygame.display.set_caption('Drawing')

    def update(self):
        # draw on the surface object
        self.DISPLAYSURF.fill(self.WHITE)

        for node in nx.nodes(self.map.graph):
            if node.z != self.layer:
                continue
            pygame.draw.circle(self.DISPLAYSURF, self.BLUE, node.xy_display(self.scale), 5, 0)

        for edge in nx.edges(self.map.graph):
            pygame.draw.line(self.DISPLAYSURF, self.GREEN, edge[0].xy_display(self.scale), edge[1].xy_display(self.scale), 2) 

        pygame.display.update()


class Input(object):
    def __init__(self):
        pass

    def process(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                print event.key, event.unicode
        

    

min = 0
max = 10
scale = 100

map = Map(max)
display = Display(map, scale)
input = Input()
            
map.print_grid()
print "================================="

  
  

# run the game loop
while True:
    input.process()
    display.update()


