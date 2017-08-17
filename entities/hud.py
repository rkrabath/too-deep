#!/usr/bin/python

import sys
import networkx as nx
import pygame
import math
from pygame.locals import *

from point import Point
import map as map_object

class HUD(object):

    def __init__(self):
        pygame.font.init()

        self.scale = 20
        self.font = pygame.font.SysFont("fake", 28, True)
        self.background_color = pygame.Color(0,0,0,168)
        self.border_color = pygame.Color(0,0,0)
        self.text_color = pygame.Color(0,128,0)

        self.message = ["Welcome!  Don't dig too deep!"]


        
    def points_selected(self):
        self.message = [
                "Options:",
                "  S for stairs",
                "  T for tunnel",
                "  D for ditch",
                "  R for ramp",
                ]


    def clear(self):
        self.message = []


    def draw_hud_box(self, width, height):
        hud_canvas = pygame.Surface((width, height),pygame.SRCALPHA)

        # Setup rectangles
        top_left_rect = pygame.Rect(0,0,self.scale,self.scale)
        top_right_rect = pygame.Rect(width-self.scale,0,self.scale,self.scale)
        bottom_left_rect = pygame.Rect(0,height-self.scale,self.scale,self.scale)
        bottom_right_rect = pygame.Rect(width-self.scale,height-self.scale,self.scale,self.scale)

        # Draw shaded background
        pygame.draw.arc(hud_canvas, self.background_color, top_left_rect, math.pi/2, math.pi, self.scale/2)
        pygame.draw.arc(hud_canvas, self.background_color, top_right_rect, 0, math.pi/2, self.scale/2)
        pygame.draw.arc(hud_canvas, self.background_color, bottom_left_rect, math.pi, 3*math.pi/2 ,self.scale/2)
        pygame.draw.arc(hud_canvas, self.background_color, bottom_right_rect, 3*math.pi/2.0, 2*math.pi, self.scale/2)
        pygame.draw.rect(hud_canvas, self.background_color, (self.scale/2.0, 0, width-self.scale, height))
        pygame.draw.rect(hud_canvas, self.background_color, (0, self.scale/2.0, self.scale, height-self.scale))
        pygame.draw.rect(hud_canvas, self.background_color, (width-self.scale/2.0, self.scale/2.0, width, height-self.scale))

        # Draw box outline
        pygame.draw.arc(hud_canvas, self.border_color, top_left_rect, math.pi/2.0, math.pi, 5)
        pygame.draw.arc(hud_canvas, self.border_color, top_right_rect, 0, math.pi/2.0, 5)
        pygame.draw.arc(hud_canvas, self.border_color, bottom_left_rect, math.pi, 3*math.pi/2.0 ,5)
        pygame.draw.arc(hud_canvas, self.border_color, bottom_right_rect, 3*math.pi/2.0, 2*math.pi, 5)
        pygame.draw.line(hud_canvas, self.border_color, (self.scale/2, 0), (width-self.scale/2,0), 5)
        pygame.draw.line(hud_canvas, self.border_color, (self.scale/2, height), (width-self.scale/2,height), 5)
        pygame.draw.line(hud_canvas, self.border_color, (0, self.scale/2), (0, height-self.scale/2), 5)
        pygame.draw.line(hud_canvas, self.border_color, (width, self.scale/2), (width,height-self.scale/2), 5)

        return hud_canvas

    
    def draw_hud_text(self):
        return [self.font.render(line, True, self.text_color) for line in self.message]


    def get_hud(self):

        if not self.message:
            return pygame.Surface((0,0))

        width = 0
        height = 0
        for line in self.message:
            new_width, new_height = self.font.size(line)
            width = max(width, new_width)
            height += new_height

        # Add padding
        height += 20 
        width += 20 
        
        box = self.draw_hud_box(width, height)
        text = self.draw_hud_text()

        x = 10
        y = 10
        for line in text:
            box.blit(line, (x,y))
            y += line.get_height()

        return box



