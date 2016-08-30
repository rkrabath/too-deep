import entities as e
import unittest
import os
from time import sleep

class TestItem(unittest.TestCase):
#	def setUp(self):
#		pass
	
	def test_item_creation(self):
		e.item.Item('food/meat/shank')
		

	
