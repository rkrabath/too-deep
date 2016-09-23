import entities as e
import unittest
import os
from time import sleep

#
# 1---+          
# | A |     7-+
# |   |     |D|  9---+
# |   |     | |  |E  |
# |   3-----+-8  |   |
# |   | B   |    +---0
# +---2   5-|--+
#     |   | |C |
#     |   +-|--6
#     +-----4

# 1: (1,1)
# 2: (5,7)
# 3: (5,5)
# 4: (11,10)
# 5: (9,7)
# 6: (14,9)
# 7: (11,2)
# 8: (13,5)
# 9: (16,3)
# 0: (20,6)

class TestBox(unittest.TestCase):
    def setUp(self):
        self.A = e.Box(e.Point(0,1,1),e.Point(0,5,7))
        self.B = e.Box(e.Point(0,5,5),e.Point(0,11,10))
        self.C = e.Box(e.Point(0,9,7),e.Point(0,14,9))
        self.D = e.Box(e.Point(0,11,2),e.Point(0,13,4))
        self.E = e.Box(e.Point(0,16,3),e.Point(0,20,6))
	

    def test_box_error_handling(self):
        self.assertRaises(TypeError, e.Box, (4))
        self.assertRaises(TypeError, e.Box, ([4,4]))
        self.assertRaises(ValueError, e.Box, e.Point(0,4,4), (0,4,4))
        self.assertRaises(ValueError, e.Box, (4,4,4), e.Point(0,4,4))


    def test_adjacency(self):
        assert self.A.adjecent_to(self.B)
        assert not self.D.adjecent_to(self.E)
        assert not self.B.adjecent_to(self.C)

    def test_overlapping(self):
        assert self.B.is_overlapping(self.C)
        assert not self.A.is_overlapping(self.B)
        assert not self.B.is_overlapping(self.D)
        assert not self.B.is_overlapping(self.E)
        assert not self.D.is_overlapping(self.C)
        assert not self.D.is_overlapping(self.E)


	
