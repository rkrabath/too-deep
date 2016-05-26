import entities as e
import unittest
import os
from time import sleep


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


	def test_process(self):
		self.input.process()
