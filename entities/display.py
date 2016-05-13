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
        self.underground_texture = pygame.image.load('graphics/underground_tiles.png')
        self.textures = {}
        self.textures['full_full'] = pygame.Rect(32,64,32,32)
        self.textures['full_left'] = pygame.Rect(0,64,32,32)
        self.textures['full_right'] = pygame.Rect(64,64,32,32)
        self.textures['bottom_full'] = pygame.Rect(32,96,32,32)
        self.textures['top_full'] = pygame.Rect(32,32,32,32)
        self.textures['bottom_right'] = pygame.Rect(64,96,32,32)
        self.textures['bottom_left'] = pygame.Rect(0,96,32,32)
        self.textures['top_right'] = pygame.Rect(64,32,32,32)
        self.textures['top_left'] = pygame.Rect(0,32,32,32)
        self.textures['topbottom'] = pygame.Rect(64,128,32,32)
        self.textures['rightleft'] = pygame.Rect(0,128,32,32)
        self.textures['topbottom_left'] = pygame.Rect(0,160,32,32)
        self.textures['topbottom_right'] = pygame.Rect(64,160,32,32)
        self.textures['top_rightleft'] = pygame.Rect(32,128,32,32)
        self.textures['bottom_rightleft'] = pygame.Rect(32,192,32,32)
        self.textures['no_path'] = pygame.Rect(32,160,32,32)
        self.dwarves = pygame.image.load('graphics/dwarves.png')
        self.items = pygame.image.load('graphics/items.png')

        # set up the window
        pygame.display.set_caption('Too Deep')


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
            self.DISPLAYSURF.blit(self.dwarves, agent.location.xy_display_offset(self.scale), area=pygame.Rect(0,0,32,32))


    def draw_items(self):
        for item in self.dispatch.items:
            self.DISPLAYSURF.blit(self.items, item.location.xy_display_offset(self.scale), area=item.sprite)

    
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
            left = node.left_neighbor() in incomming_links
            right = node.right_neighbor() in incomming_links
            top = node.top_neighbor() in incomming_links
            bottom = node.bottom_neighbor() in incomming_links
            draw_loc = node.xy_display_offset(self.scale)
            if top and bottom and left and right:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['full_full'])
            elif top and bottom and left:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['full_right'])
            elif top and bottom and right:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['full_left'])
            elif top and left and right:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['bottom_full'])
            elif bottom and left and right:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['top_full'])
            elif top and left:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['bottom_right'])
            elif top and right:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['bottom_left'])
            elif bottom and left:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['top_right'])
            elif bottom and right:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['top_left'])
            elif bottom and top:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['rightleft'])
            elif right and left:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['topbottom'])
            elif right:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['topbottom_left'])
            elif left:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['topbottom_right'])
            elif top:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['bottom_rightleft'])
            elif bottom:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['top_rightleft'])
            else:
                self.DISPLAYSURF.blit(self.underground_texture, draw_loc, area=self.textures['no_path'])

        # for edge in nx.edges(self.map.graph):
        #     if edge[0].z != self.layer or edge[1].z != self.layer:
        #         continue
        #     pygame.draw.line(self.DISPLAYSURF, self.GREEN, edge[0].xy_display(self.scale), edge[1].xy_display(self.scale), 1) 
        self.draw_items()

        self.draw_agents()

        self.show_highlight()
    
        pygame.display.update()

