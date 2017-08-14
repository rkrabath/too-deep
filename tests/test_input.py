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

                expected = e.Pointset([(0,5,5), (0,5,6), (0,5,7), (0,6,5), (0,6,6), (0,6,7), (0,7,5), (0,7,6), (0,7,7)])

                assert self.input.selections.points == expected.points

        def test_normalize_box(self):
                a = (1,1)
                b = (1,4)
                c = (4,1)
                d = (4,4)

                assert self.input.normalize_box((a,d)) == (a,d)
                assert self.input.normalize_box((d,a)) == (a,d)
                assert self.input.normalize_box((b,c)) == (a,d)
            
