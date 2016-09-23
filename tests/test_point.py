import entities as e
import unittest
import os
from time import sleep

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.test_point = e.Point(1,2,3)
	
    def test_xy(self):
        assert self.test_point.xy() == (2,3)

    def test_right_neighbor(self):
        assert self.test_point.right_neighbor() == e.Point(1,3,3)
	
    def test_bottom_neighbor(self):
        assert self.test_point.bottom_neighbor() == e.Point(1,2,4)
