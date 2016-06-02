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
                dispatch_object = e.Dispatch()
                display_object = e.Display(10)
		self.input = e.Input(display_object, dispatch_object)


	def test_exit(self):
		self.assertRaises(SystemExit, self.input.exit)


	def test_key_process(self):
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': '>',
                            'key': '>',
                            'mod': '>',
                            }))
                pygame.event.post(pygame.event.Event(KEYDOWN, {
                            'unicode': '?',
                            'key': '?',
                            'mod': '?',
                            }))
		self.input.process()


	def test_exiting(self):
                pygame.event.post(pygame.event.Event(QUIT))
		self.assertRaises(SystemExit, self.input.process)
