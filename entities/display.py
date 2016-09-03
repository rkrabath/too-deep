#!/usr/bin/python

import sys
import networkx as nx
import pygame
from pygame.locals import *

from point import Point
import map as map_object

class Display(object):

    def __init__(self, scale):
        # set up the colors
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.RED   = (255,   0,   0)
        self.GREEN = (  0, 255,   0)
        self.BLUE  = (  0,   0, 255)
        pygame.init()
        self.scale = scale
        self.map = map_object
        self.layer = self.map.layer_max
        self.highlighted_coordinate = None
        self.highlighted_selections = None
    
        dimension = self.scale * self.map.layer_max + 2
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
        self.item_sprites = pygame.image.load('graphics/items.png')

        # set up the window
        pygame.display.set_caption('Too Deep')


    def level_down(self):
        if not self.layer - 1 < self.map.layer_min:
            self.layer -= 1

        
    def level_up(self):
        if not self.layer + 1 > self.map.layer_max:
            self.layer += 1


    def get_coord(self, point):
        """ Translate display points to map points """
        offset = self.scale/2
        # offset, round considerably (integer division)
        
        protopoint = [(sub+offset)/self.scale for sub in point]
        return Point(self.layer, *protopoint)
        

    def draw_agents(self, agents):
        for agent in agents:
            self.DISPLAYSURF.blit(self.dwarves, agent.location.xy_display_offset(self.scale), area=pygame.Rect(0,0,32,32))


    def draw_items(self, items):
        for item in items:
            try:
                location = item[1].location.xy_display_offset(self.scale)
            except IndexError:
                continue
            self.DISPLAYSURF.blit(self.item_sprites, location, area=item.sprite)

    
    def highlight_node(self, xy):
        self.highlighted_coordinate = xy


    def highlight_selections(self, selections):
        print selections
        self.highlighted_selections = selections


    def show_highlight(self):
        if self.highlighted_coordinate:
            display_point = [(x*self.scale-self.scale/2) for x in self.highlighted_coordinate]
            #print "Cursor highlight at {0}".format(str(display_point))
            s = pygame.Surface((self.scale,self.scale))
            s.set_alpha(128)
            s.fill(self.RED)
            self.DISPLAYSURF.blit(s, display_point)
        if self.highlighted_selections:
            for selection in self.highlighted_selections:
                start_point = self.top_left_pixel(selection[0])
                end_point = self.bottom_right_pixel(selection[1])
                width = end_point[0] - start_point[0]
                height = end_point[1] - start_point[1]
                #print "Drawing box from {0} to {1}".format(str(start_point), str(end_point))
                s = pygame.Surface((width,height))
                s.set_alpha(96)
                s.fill(self.RED)
                self.DISPLAYSURF.blit(s, start_point)


    def update(self, agents, items):
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
        self.draw_items(items)

        self.draw_agents(agents)

        self.show_highlight()
    
        pygame.display.update()

    def top_left_pixel(self, graph_xy):
        x, y = graph_xy
        midpoint = self.scale/2
        pixel_x = (x * self.scale) - midpoint
        pixel_y = (y * self.scale) - midpoint
        pixel_xy = (pixel_x, pixel_y)
        return pixel_xy
    
    def bottom_right_pixel(self, graph_xy):
        x, y = graph_xy
        midpoint = self.scale/2
        pixel_x = (x * self.scale) + midpoint
        pixel_y = (y * self.scale) + midpoint
        pixel_xy = (pixel_x, pixel_y)
        return pixel_xy
        
