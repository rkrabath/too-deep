#!/usr/bin/python

import sys
import pygame
import multiprocessing
import networkx as nx
from pygame.locals import *

from agent import Agent
from point import Point

class Dispatch(object):
    def __init__(self, map):
        self.agents = {}
        self.exit = None
        self.map = map
        
        self.iterator = self.auto_increment()

        middle = map.max/2
        self.create_exit_at(Point(map.max, middle, middle))
        print Point(map.max, middle, middle)


    
    def auto_increment(self):
        next_value = 0
        while True:
            yield next_value
            next_value += 1


    def update(self):
        to_remove = []
        for index, agent in self.agents.iteritems():
            entity, pipe, location = agent
            pipe.send({'command': 'tick'})
            while pipe.poll():
                message = pipe.recv()
                if message['command'] == 'new_position':
                    location = message['payload']
                    self.agents[index] = [entity, pipe, location]
                if message['command'] == 'kill_me':
                    pipe.send({'command': 'die'})
                    entity.cleanup()
                    to_remove.append(index)


        for dearly_departed in set(to_remove):
            del self.agents[dearly_departed]

      

    def create_agent_at(self, location):
        dispatch_end, agent_end = multiprocessing.Pipe()
        agent = Agent(agent_end, location)
        dispatch_end.send({'command': 'update_map', 'payload': self.map.graph})
        self.agents[self.iterator.next()] = [agent, dispatch_end, location]
    

    def create_exit_at(self, location):
        if self.exit:
            raise ValueError('The exit was already placed.')
        self.exit = location


    def find(self, thing):
        if thing == 'exit':
            return self.exit
