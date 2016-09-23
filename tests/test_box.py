import entities as e
import unittest
import os
from time import sleep

class TestBox(unittest.TestCase):
#    def setUp(self):
	
    def test_box_error_handling(self):
        self.assertRaises(TypeError, e.Box, (4))
        self.assertRaises(TypeError, e.Box, ([4,4]))
        self.assertRaises(ValueError, e.Box, e.Point(0,4,4), (0,4,4))
        self.assertRaises(ValueError, e.Box, (4,4,4), e.Point(0,4,4))


    def test_compound_box_creation(self):
        box1 = e.Box(e.Point(0,4,4),e.Point(0,5,5))
        box2 = e.Box(e.Point(0,4,4),e.Point(0,4,5))
        box3 = e.Box(e.Point(0,4,5),e.Point(0,6,6))

        result_1 = type(e.CompoundBox(box1).original_boxes)
        result_2 = type(e.CompoundBox([box1, box2, box3]).original_boxes)

#        assert result_1 == self.intended_type
#        assert result_2 == self.intended_type
		
#    def test_compound_box_computation(self):
#        boxes = 

	
