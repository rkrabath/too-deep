import entities as e
import unittest
import os
from time import sleep

class TestInput(unittest.TestCase):
        def setUp(self):
                map_object = e.Map(10)
                dispatch_object = e.Dispatch(map_object)
                display_object = e.Display(map_object, 10)
		self.input = e.Input(display_object, dispatch_object)


	def test_exit(self):
		self.assertRaises(SystemExit, self.input.exit)


	def test_process(self):
		self.input.process()
