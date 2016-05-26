import entities as e
import unittest
import os
from time import sleep


class TestDisplay(unittest.TestCase):
        def setUp(self):
		game_map = e.map
                try:
                        game_map.init(10)
                except ValueError:
                        pass # Already initialized in earlier test
                self.display = e.Display(10)


        def tearDown(self):
		self.display = None

	def test_instantiation(self):
		print self.display.scale

	def test_level_up_down(self):
		# Down a level
		old_level = self.display.layer
		self.display.level_down()
		new_level = self.display.layer
		assert new_level != old_level

		# Up a level
		old_level = self.display.layer
		self.display.level_up()
		new_level = self.display.layer
		assert new_level != old_level

	def test_highlight(self):
		self.display.highlight_node(e.Point(10,1,1))
		self.display.show_highlight()

	def test_update(self):
		old_image = self.display.DISPLAYSURF.get_buffer().raw
		self.display.highlight_node(e.Point(10,2,2))
		self.display.update([],[])
		new_image = self.display.DISPLAYSURF.get_buffer().raw
		assert old_image != new_image


	
