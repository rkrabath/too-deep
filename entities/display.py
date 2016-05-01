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
        self.surface_texture = pygame.image.load('graphics/surface_tiles.png')
        self.underground_textures = {}
        self.underground_textures['full_full'] = pygame.image.load('graphics/floor_full_full.png')
        self.underground_textures['full_left'] = pygame.image.load('graphics/wall_left.png')
        self.underground_textures['full_right'] = pygame.image.load('graphics/wall_right.png')
        self.underground_textures['bottom_full'] = pygame.image.load('graphics/wall_bottom.png')
        self.underground_textures['top_full'] = pygame.image.load('graphics/wall_top.png')
        self.underground_textures['bottom_right'] = pygame.image.load('graphics/wall_bottom_right.png')
        self.underground_textures['bottom_left'] = pygame.image.load('graphics/wall_bottom_left.png')
        self.underground_textures['top_right'] = pygame.image.load('graphics/wall_top_right.png')
        self.underground_textures['top_left'] = pygame.image.load('graphics/wall_top_left.png')
        self.underground_textures['topbottom'] = pygame.image.load('graphics/wall_topbottom.png')
        self.underground_textures['rightleft'] = pygame.image.load('graphics/wall_rightleft.png')
        self.underground_textures['topbottom_left'] = pygame.image.load('graphics/wall_topbottom_left.png')
        self.underground_textures['topbottom_right'] = pygame.image.load('graphics/wall_topbottom_right.png')
        self.underground_textures['top_rightleft'] = pygame.image.load('graphics/wall_top_rightleft.png')
        self.underground_textures['bottom_rightleft'] = pygame.image.load('graphics/wall_bottom_rightleft.png')
        self.underground_textures['stone'] = pygame.image.load('graphics/stone.png')

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
            incomming_links = self.map.get_incident_edges(node)
            print "Layer: {0}".format(self.layer)
            print "Node: {0}".format(node)
            print "Neighbors: {0}".format(incomming_links)
            left = node.left_neighbor() in incomming_links
            right = node.right_neighbor() in incomming_links
            top = node.top_neighbor() in incomming_links
            bottom = node.bottom_neighbor() in incomming_links
            if top and bottom and left and right:
                self.DISPLAYSURF.blit(self.underground_textures['full_full'], node.xy_display_offset(self.scale))
            elif top and bottom and left:
                self.DISPLAYSURF.blit(self.underground_textures['full_right'], node.xy_display_offset(self.scale))
            elif top and bottom and right:
                self.DISPLAYSURF.blit(self.underground_textures['full_left'], node.xy_display_offset(self.scale))
            elif top and left and right:
                self.DISPLAYSURF.blit(self.underground_textures['bottom_full'], node.xy_display_offset(self.scale))
            elif bottom and left and right:
                self.DISPLAYSURF.blit(self.underground_textures['top_full'], node.xy_display_offset(self.scale))
            elif top and left:
                self.DISPLAYSURF.blit(self.underground_textures['bottom_right'], node.xy_display_offset(self.scale))
            elif top and right:
                self.DISPLAYSURF.blit(self.underground_textures['bottom_left'], node.xy_display_offset(self.scale))
            elif bottom and left:
                self.DISPLAYSURF.blit(self.underground_textures['top_right'], node.xy_display_offset(self.scale))
            elif bottom and right:
                self.DISPLAYSURF.blit(self.underground_textures['top_left'], node.xy_display_offset(self.scale))
            elif bottom and top:
                self.DISPLAYSURF.blit(self.underground_textures['rightleft'], node.xy_display_offset(self.scale))
            elif right and left:
                self.DISPLAYSURF.blit(self.underground_textures['topbottom'], node.xy_display_offset(self.scale))
            elif right:
                self.DISPLAYSURF.blit(self.underground_textures['topbottom_left'], node.xy_display_offset(self.scale))
            elif left:
                self.DISPLAYSURF.blit(self.underground_textures['topbottom_right'], node.xy_display_offset(self.scale))
            elif top:
                self.DISPLAYSURF.blit(self.underground_textures['bottom_rightleft'], node.xy_display_offset(self.scale))
            elif bottom:
                self.DISPLAYSURF.blit(self.underground_textures['top_rightleft'], node.xy_display_offset(self.scale))
            else:
                self.DISPLAYSURF.blit(self.underground_textures['stone'], node.xy_display_offset(self.scale))
                
                
                
            
                
            
            
# Layer: 32
# Node: (32,2,30)
# Neighbors: [(32,3,30), (32,2,29), (32,1,30), (32,2,31)]

            
            

        for edge in nx.edges(self.map.graph):
            if edge[0].z != self.layer or edge[1].z != self.layer:
                continue
            pygame.draw.line(self.DISPLAYSURF, self.GREEN, edge[0].xy_display(self.scale), edge[1].xy_display(self.scale), 1) 

        self.draw_agents()

        self.draw_exit()

        self.show_highlight()
    
        pygame.display.update()

