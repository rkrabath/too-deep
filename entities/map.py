import sys
import networkx as nx
import pygame
from pygame.locals import *

from point import Point


graph = nx.Graph()
layer_min = 0
layer_max = None


def init(new_layer_max=None):
    global layer_max

    if not layer_max: # First instantiation
        if new_layer_max: # caller has provided desired max size
            layer_max = new_layer_max
    
            # Create nodes for topmost layer:
            for x in range(layer_min, layer_max+1):
                for y in range(layer_min, layer_max+1):
                    # add node:
                    p = Point(layer_max,x,y)
                    graph.add_node(p)
    
            # Create connections for topmost layer:
            for x in range(layer_min, layer_max+1):
                for y in range(layer_min, layer_max+1):
                    make_traversable(Point(layer_max,x,y), setup=True)
        else: # First instiantiation, no value provided.
            raise ValueError("Must provide size of map upon initial instantiation!")
    else: # subsequent instantian
        if new_layer_max:
            raise ValueError("Can't change the map size once it's been instantiated!")
            


def print_grid():
    for node in nx.nodes(graph):
        print node
        for neighbor in nx.all_neighbors(graph, node):
            print " " + str(neighbor)


def get_incident_edges(node):
    try:
        return [x for x in nx.all_neighbors(graph, node)]
    except nx.exception.NetworkXError:
        return []
        

def is_traversable(node):
    if get_incident_edges(node):
        return True
    else:
        return False


def make_traversable(node, setup=False):
    try:
        west_point = Point(node.z,node.x-1,node.y)
        if is_traversable(west_point) or setup:
            graph.add_edge(node,west_point)
    except ValueError:
        pass

    try:
        south_point = Point(node.z,node.x,node.y-1)
        if is_traversable(south_point) or setup:
            graph.add_edge(node,south_point)
    except ValueError:
        pass

    east_point = Point(node.z,node.x+1,node.y)
    if node.x != max:
        if is_traversable(east_point) or setup:
            graph.add_edge(node,east_point)

    north_point = Point(node.z,node.x,node.y+1)
    if node.y != max:
        if is_traversable(north_point) or setup:
            graph.add_edge(node,north_point)
    

def make_not_traversable(node):
    for neighbor in graph.neighbors(node):        
        graph.remove_edge(neighbor, node)


