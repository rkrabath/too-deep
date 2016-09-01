import entities as e
import unittest
import os
from time import sleep

class TestDispatch(unittest.TestCase):
	def setUp(self):
		self.dispatch_object = e.Dispatch()

	
	def test_create_agent_and_exit(self):
		self.dispatch_object.create_agent_at(e.Point(10,1,1))
		assert self.dispatch_object.agents[0].location == e.Point(10,1,1)
		self.dispatch_object.exit()
		self.dispatch_object.update()
		assert self.dispatch_object.agents == []


	def test_create_item(self):
		self.dispatch_object.create_item_at('food/meat/shank', e.Point(10,1,1))
		assert self.dispatch_object.items[0][1] == e.Point(10,1,1)


	def test_update(self):
		self.dispatch_object.update()

		

	
