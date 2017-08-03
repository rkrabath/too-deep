import entities as e
import unittest
import os
from time import sleep

class TestCompoundBox(unittest.TestCase):
    def setUp(self):
        self.intended_type = type([])
	
#    def test_compound_box_error_handling(self):
#        self.assertRaises(ValueError, e.CompoundBox, (4))
#        self.assertRaises(ValueError, e.CompoundBox, ([4,4,4]))
#
#
#    def test_compound_box_creation(self):
#        box1 = e.Box(e.Point(0,4,4),e.Point(0,5,5))
#        box2 = e.Box(e.Point(0,4,4),e.Point(0,4,5))
#        box3 = e.Box(e.Point(0,4,5),e.Point(0,6,6))
#
#        result_1 = type(e.CompoundBox(box1).original_boxes)
#        result_2 = type(e.CompoundBox([box1, box2, box3]).original_boxes)
#
#        assert result_1 == self.intended_type
#        assert result_2 == self.intended_type
#
#    def test_compound_box_overlapping_1_corner(self):
#        # one corner overlapping boxes:
#
#        # A---*
#        # |   |
#        # | C-+-*
#        # | | | |
#        # *-+-B |
#        #   |   |
#        #   *---D
#        #
#
#        # Should return:
#
#        # 
#        # 
#        #     A-*
#        #     | |
#        #   C---B
#        #   |   |
#        #   *---D
#        #
#
#
#        box1 = e.Box(e.Point(0,0,0), e.Point(0,4,4))
#        box2 = e.Box(e.Point(0,2,2), e.Point(0,6,6))
#        orig = e.CompoundBox(box1)
#
#        resultbox1 = e.Box(e.Point(0,4,2), e.Point(0,6,4))
#        resultbox2 = e.Box(e.Point(0,2,4), e.Point(0,6,6))
#        intended_result = [resultbox1, resultbox2]
#
#        result = orig._non_overlapping_peices_(box2)
#
#        assert result == intended_result
#
#
#    def test_compound_box_overlapping_2_corners(self):
#        # two corner overlapping boxes:
#
#        # A-------*
#        # |       |
#        # | C---* |
#        # | |   | |
#        # *-+---+-B
#        #   |   |
#        #   *---D
#        #
#
#        # Should return:
#
#        # 
#        # 
#        #        
#        #        
#        #   A---*
#        #   |   |
#        #   *---B
#        #
#
#        box1 = e.Box(e.Point(0,0,0), e.Point(0,8,4))
#        box2 = e.Box(e.Point(0,2,2), e.Point(0,6,6))
#        orig = e.CompoundBox(box1)
#
#        resultbox = e.Box(e.Point(0,2,4), e.Point(0,6,6))
#        intended_result = [resultbox]
#
#        result = orig._non_overlapping_peices_(box2)
#
#        assert result == intended_result
#
#
#    def test_compound_box_overlapping_2_corners_opposite(self):
#        # two corner overlapping boxes:
#
#        #          
#        #   A---*  
#        #   |   |  
#        # C-+---+-*
#        # | |   | |
#        # | *---B |
#        # |       |
#        # *-------D
#
#        # Should return:
#
#        # 
#        #          
#        #          
#        #          
#        # A-*   E-*
#        # | |   | |
#        # C-B---*-F
#        # |       |
#        # *-------D
#        # 
#
#        box1 = e.Box(e.Point(0,3,1), e.Point(0,7,5))
#        box2 = e.Box(e.Point(0,1,3), e.Point(0,9,7))
#        orig = e.CompoundBox(box1)
#
#        resultbox1 = e.Box(e.Point(0,1,3), e.Point(0,3,5))
#        resultbox2 = e.Box(e.Point(0,1,5), e.Point(0,9,7))
#        resultbox3 = e.Box(e.Point(0,7,5), e.Point(0,9,5))
#        intended_result = [resultbox1, resultbox2, resultbox3]
#
#        result = orig._non_overlapping_peices_(box2)
#
#        assert result == intended_result
#
#
#    def test_compound_box_overlapping_3_corners(self):
#        # two corner overlapping boxes:
#
#        # A---------*
#        # |   E---* |
#        # | C-+-* | |
#        # | | | | | |
#        # *-+-+-+-+-B
#        #   | | | |
#        #   | *-+-F
#        #   |   |
#        #   *---D
#
#        # Should return:
#
#        #            
#        #            
#        #            
#        #            
#        #       A-*  
#        #       | |
#        #       +-B
#        #        
#
#        box1 = e.Box(e.Point(0,0,0), e.Point(0,10,4))
#        box2 = e.Box(e.Point(0,2,2), e.Point(0,6,8))
#        box3 = e.Box(e.Point(0,4,1), e.Point(0,8,6))
#        orig = e.CompoundBox([box1, box2])
#        
#        intended_result = [e.Box(e.Point(0,6,4), e.Point(0,8,6))]
#
#        result = orig._non_overlapping_peices_(box3)
#
#        assert result == intended_result
#
#    def test_compound_box_overlapping_4_corners(self):
#        # two corner overlapping boxes:
#
#        # A---------*
#        # | C--*    |
#        # | |  |    |
#        # | *--D    |
#        # *---------B
#        #
#
#        # Should return:
#
#        #            
#
#        box1 = e.Box(e.Point(0,0,0), e.Point(0,10,5))
#        box2 = e.Box(e.Point(0,2,2), e.Point(0,4,4))
#        orig = e.CompoundBox(box1)
#
#        intended_result = None
#
#        result = orig._non_overlapping_peices_(box2)
#
#        assert result == intended_result
		
	
