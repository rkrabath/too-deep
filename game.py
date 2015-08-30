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
    def __init__(self,max):
        self.graph = nx.Graph()
        self.min = 0
        self.max = max

        # Create nodes for topmost layer:
        for x in range(self.min,self.max+1):
            for y in range(self.min,self.max+1):
                # add node:
                p = Point(max,x,y)
                self.graph.add_node(p)

        # Create connections for topmost layer:
        for x in range(self.min,self.max+1):
            for y in range(self.min,self.max+1):
                p = Point(max,x,y)
                # compute neighbors:
                south_point = Point(max,x,y-1)
                west_point = Point(max,x-1,y)
                
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
        return [(sub+offset)/scale for sub in point]
        

    def highlight_node(self, point):
        self.highlighted_coordinate = point


    def show_highlight(self):
        if self.highlighted_coordinate:
            display_point = [(x*scale-self.scale/2) for x in self.highlighted_coordinate]
            s = pygame.Surface((100,100))
            s.set_alpha(128)
            s.fill(self.RED)
            self.DISPLAYSURF.blit(s, display_point)


    def update(self):
        # draw on the surface object
        self.DISPLAYSURF.fill(self.WHITE)

        for node in nx.nodes(self.map.graph):
            if node.z != self.layer:
                continue
            pygame.draw.circle(self.DISPLAYSURF, self.BLUE, node.xy_display(self.scale), 5, 0)

        for edge in nx.edges(self.map.graph):
            if node.z != self.layer:
                continue
            pygame.draw.line(self.DISPLAYSURF, self.GREEN, edge[0].xy_display(self.scale), edge[1].xy_display(self.scale), 2) 

        self.show_highlight()
    
        pygame.display.update()


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
                print "Clicked on " + ", ".join([str(x) for x in node])
            else:
                print "Unrecongized entry: ", event.type
    

min = 0
max = 10
scale = 100

map = Map(max)
display = Display(map, scale)
input = Input(display)
            
#map.print_grid()
print K_LESS
print K_GREATER
print "================================="



# run the game loop
while True:
    input.process()
    display.update()


