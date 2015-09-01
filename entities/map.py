#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

from point import Point

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
                self.make_traversable(Point(max,x,y))
                

    def print_grid(self):
        for node in nx.nodes(self.graph):
            print node
            for neighbor in nx.all_neighbors(self.graph, node):
                print " " + str(neighbor)


    def get_incident_edges(self, node):
        try:
            return [x for x in nx.all_neighbors(self.graph, node)]
        except nx.exception.NetworkXError:
            return []
            

    def is_traversable(self, node):
        if self.get_incident_edges(node):
            return True
        else:
            return False


    def make_traversable(self, node):
        try:
            west_point = Point(node.z,node.x-1,node.y)
            self.graph.add_edge(node,west_point)
        except ValueError:
            pass

        try:
            south_point = Point(node.z,node.x,node.y-1)
            self.graph.add_edge(node,south_point)
        except ValueError:
            pass

        east_point = Point(node.z,node.x+1,node.y)
        if node.x != max:
            self.graph.add_edge(node,east_point)

        north_point = Point(node.z,node.x,node.y+1)
        if node.y != max:
            self.graph.add_edge(node,north_point)
        

    def make_not_traversable(self, node):
        north_point = Point(node.z,node.x,node.y+1)
        south_point = Point(node.z,node.x,node.y-1)
        east_point = Point(node.z,node.x+1,node.y)
        west_point = Point(node.z,node.x-1,node.y)

        for neighbor in self.graph.neighbors(node):        
            self.graph.remove_edge(neighbor, node)
        

