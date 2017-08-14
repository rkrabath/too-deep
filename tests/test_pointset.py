import entities as e
import unittest
import os
from time import sleep

class TestPointset(unittest.TestCase):
    def setUp(self):
        #self.test_point = e.Point(1,2,3)
        self.ps = e.Pointset()
	
    def test_add_point(self):
        self.ps += e.Point(0,1,1)
        assert self.ps.points == set([e.Point(0,1,1)])

    def test_add_pointset(self):
        new_ps = e.Pointset([e.Point(0,1,1), e.Point(0,1,2), e.Point(0,1,3)])
        self.ps += new_ps
        assert self.ps.points == new_ps.points

    def test_sub_point(self):
        self.ps -= e.Point(0,1,1)
        assert self.ps.points == set([])

    def test_sub_pointset(self):
        new_ps = e.Pointset([e.Point(0,1,1), e.Point(0,1,2), e.Point(0,1,3)])
        self.ps -= new_ps
        assert self.ps.points == set([])

