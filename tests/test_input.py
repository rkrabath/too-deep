import entities as e
import unittest
import os
from time import sleep

import pygame
from pygame.locals import *


class TestInput(unittest.TestCase):
        def setUp(self):
                game_map = e.map
		try:
			game_map.init(10)
		except ValueError:
			pass # Already initialized in earlier test
                self.dispatch_object = e.Dispatch()
                display_object = e.Display(10)
		self.input = e.Input(display_object, self.dispatch_object)

        
        def tearDown(self):
            for agent in self.dispatch_object.agents:
                agent.exit()


	def test_exit(self):
		self.assertRaises(SystemExit, self.input.exit)


	def test_key_process(self):
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': '>',
                            'key': 46,
                            'mod': '>',
                            }))
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': '?',
                            'key': '?',
                            'mod': '?',
                            }))
		self.input.process()

        
        def test_mouse_button(self):
                # Toggle barrier on
                pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN, {
                            'pos': [0,0],
                            'button': 1,
                            }))
                # place agent
                pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN, {
                            'pos': [5,5],
                            'button': 3,
                            }))
                # Toggle barrier off
                pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN, {
                            'pos': [0,0],
                            'button': 1,
                            }))
		self.input.process()


        def test_unhandled_input(self):
                # unknown input
                pygame.event.post(pygame.event.Event(VIDEOEXPOSE, {
                            }))
		self.input.process()


	def test_exiting(self):
                pygame.event.post(pygame.event.Event(QUIT))
		self.assertRaises(SystemExit, self.input.process)


        def test_box_selection(self):
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': ' ',
                            'key': 32,
                            'mod': '',
                            }))
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': '',
                            'key': 274,
                            'mod': '',
                            }))
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': '',
                            'key': 274,
                            'mod': '',
                            }))
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': '',
                            'key': 275,
                            'mod': '',
                            }))
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': '',
                            'key': 275,
                            'mod': '',
                            }))
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': ' ',
                            'key': 32,
                            'mod': '',
                            }))
		self.input.process()

                expected = e.Pointset([(0,5,6), (0,5,5), (0,6,6), (0,6,5)])

                assert self.input.selections.points == expected.points
            
