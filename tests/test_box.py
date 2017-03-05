import entities as e
import unittest
import os
from time import sleep

#
# 1---+          
# | A |     7-+
# |   |     |D|  9---+
# |   |     | |  |E  |
# |   3-----+-8  | +-|-+
# |   | B   |    +---0 |
# +---2   5-|--+   | F |
#     |   | |C |   +---+
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


# print
# print "expected:"
# print expected
# print "got:"
# print box1 - box2
# print



class TestBox(unittest.TestCase):
    def setUp(self):
        self.A = e.Box(e.Point(0,1,1),e.Point(0,5,7))
        self.B = e.Box(e.Point(0,5,5),e.Point(0,11,10))
        self.C = e.Box(e.Point(0,9,7),e.Point(0,14,9))
        self.D = e.Box(e.Point(0,11,2),e.Point(0,13,4))
        self.E = e.Box(e.Point(0,16,3),e.Point(0,20,6))
        self.F = e.Box(e.Point(0,18,5),e.Point(0,22,8))
        self.G = e.Box(e.Point(0,0,0), e.Point(0,8,4))
        self.H = e.Box(e.Point(0,2,2), e.Point(0,6,6))
        self.I = e.Box(e.Point(0,3,1), e.Point(0,4,8))

	

    def test_box_error_handling(self):
        self.assertRaises(TypeError, e.Box, (4))
        self.assertRaises(TypeError, e.Box, ([4,4]))
        self.assertRaises(ValueError, e.Box, e.Point(0,4,4), (0,4,4))
        self.assertRaises(ValueError, e.Box, (4,4,4), e.Point(0,4,4))


#    def test_adjacency(self):
#        assert self.A.adjecent_to(self.B)
#        assert not self.D.adjecent_to(self.E)
#        assert not self.B.adjecent_to(self.C)
#
#    def test_overlapping(self):
#        assert self.B.is_overlapping(self.C)
#        assert not self.A.is_overlapping(self.B)
#        assert not self.B.is_overlapping(self.D)
#        assert not self.B.is_overlapping(self.E)
#        assert not self.D.is_overlapping(self.C)
#        assert not self.D.is_overlapping(self.E)
#        assert self.E.is_overlapping(self.F)
#        assert self.F.is_overlapping(self.E)
#        assert self.G.is_overlapping(self.H)
#        assert self.H.is_overlapping(self.G)
#        assert self.H.is_overlapping(self.I)
#        assert self.I.is_overlapping(self.H)
#

    def test_addition(self):

        #   A-*
        #   |S|
        # C-+-+-----*
        # | | | O   |
        # *-+-+-----D
        #   | |
        #   | |
        #   | |
        #   | |
        #   | |
        #   *-B

        pointA = e.Point(0,2,0)
        pointB = e.Point(0,4,10)
        pointC = e.Point(0,0,2)
        pointD = e.Point(0,10,4)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,2), e.Point(0,2,4)),
                e.Box(e.Point(0,4,2), e.Point(0,10,4)),
                box1
                ]


        assert box1 + box2 == expected


    def test_subtraction_cross(self):	
        # Sometimes the boxes might cross but not actually have points inside each other
        #
        #      +--+          +--+     
        #      |S |          |O |     
        #  +---|--|---+  +---|--|---+ 
        #  | O |  |   |  | S |  |   | 
        #  +---|--|---+  +---|--|---+ 
        #      |  |          |  |     
        #      +--+          +--+     
        pointA = e.Point(0,2,0)
        pointB = e.Point(0,4,10)
        pointC = e.Point(0,0,2)
        pointD = e.Point(0,10,4)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,2,0), e.Point(0,4,2)),
                e.Box(e.Point(0,2,4), e.Point(0,4,10)),
                ]


        assert box1 - box2 == expected

        expected = [
                e.Box(e.Point(0,0,2), e.Point(0,2,4)),
                e.Box(e.Point(0,4,2), e.Point(0,10,4)),
                ]

        assert box2 - box1 == expected

    def test_subtraction_tee(self):	
        # Still overlapping:
        # A--*    
        # |S |    
        # C--+-*  
        # |  |O|  
        # *--+-D  
        # |  |    
        # *--B
        # Because even though C is not inside Box(A,B), C is on the opposite side of it than D
        pointA = e.Point(0,0,0)
        pointB = e.Point(0,4,10)
        pointC = e.Point(0,0,2)
        pointD = e.Point(0,10,4)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,0), e.Point(0,4,2)),
                e.Box(e.Point(0,0,4), e.Point(0,4,10)),
                ]

        assert box1 - box2 == expected


        #   A--*    
        #   |S |    
        # C-+--+  
        # |O|  |  
        # *-+--D  
        #   |  |    
        #   *--B
        # Because even though C is not inside Box(A,B), C is on the opposite side of it than D
        pointA = e.Point(0,2,0)
        pointB = e.Point(0,4,10)
        pointC = e.Point(0,0,2)
        pointD = e.Point(0,4,4)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,2,0), e.Point(0,4,2)),
                e.Box(e.Point(0,2,4), e.Point(0,4,10)),
                ]

        assert box1 - box2 == expected


        #  A---C---*--*
        #  | S |   |  |
        #  *---+---+--B
        #      |   |   
        #      | O |   
        #      *---D   `

        pointA = e.Point(0,0,0)
        pointB = e.Point(0,10,4)
        pointC = e.Point(0,2,0)
        pointD = e.Point(0,4,6)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,0), e.Point(0,2,4)),
                e.Box(e.Point(0,4,0), e.Point(0,10,4)),
                ]

        
        assert box1 - box2 == expected


        #       C---*
        #       | O |
        #       |   |
        #   A---+---+--*   
        #   | S |   |  |   
        #   *---*---D--B   `

        pointA = e.Point(0,0,4)
        pointB = e.Point(0,10,6)
        pointC = e.Point(0,2,0)
        pointD = e.Point(0,4,6)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,4), e.Point(0,2,6)),
                e.Box(e.Point(0,4,4), e.Point(0,10,6)),
                ]

        
        assert box1 - box2 == expected


    def test_subtraction_2_points(self):	
        # Two points inside:
        # A----*     
        # |    |     
        # |  C-+-*   
        # |  | | |   
        # |  *-+-D   
        # |    |     
        # *----B     

        pointA = e.Point(0,0,0)
        pointB = e.Point(0,4,10)
        pointC = e.Point(0,2,2)
        pointD = e.Point(0,6,6)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,0), e.Point(0,4,2)),
                e.Box(e.Point(0,0,6), e.Point(0,4,10)),
                e.Box(e.Point(0,0,2), e.Point(0,2,6)),
                ]

        assert box1 - box2 == expected

        #   A----* 
        #   |    | 
        # C-+-*  | 
        # | | |  | 
        # *-+-D  | 
        #   |    | 
        #   *----B 

        pointA = e.Point(0,4,0)
        pointB = e.Point(0,8,10)
        pointC = e.Point(0,2,2)
        pointD = e.Point(0,6,6)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,4,0), e.Point(0,8,2)),
                e.Box(e.Point(0,4,6), e.Point(0,8,10)),
                e.Box(e.Point(0,6,2), e.Point(0,8,6)),
                ]

        assert box1 - box2 == expected


        #
        #  A-----* 
        #  |     | 
        #  | C-* | 
        #  *-+-+-B 
        #    | |   
        #    *-D   
        #          

        pointA = e.Point(0,0,0)
        pointB = e.Point(0,8,4)
        pointC = e.Point(0,2,2)
        pointD = e.Point(0,6,6)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,0), e.Point(0,2,4)),
                e.Box(e.Point(0,6,0), e.Point(0,8,4)),
                e.Box(e.Point(0,2,0), e.Point(0,6,2)),
                ]

        assert box1 - box2 == expected

        #         
        #    C-*   
        #    | |   
        #  A-+-+-* 
        #  | *-D | 
        #  |     | 
        #  *-----B 
        #

        pointA = e.Point(0,0,4)
        pointB = e.Point(0,10,8)
        pointC = e.Point(0,2,2)
        pointD = e.Point(0,6,6)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,4), e.Point(0,2,8)),
                e.Box(e.Point(0,6,4), e.Point(0,10,8)),
                e.Box(e.Point(0,2,6), e.Point(0,6,8)),
                ]

        assert box1 - box2 == expected


    def test_subtraction_1_point(self):	
        # One point inside:
        # A---*   
        # |   |   
        # | C-+-* 
        # *-+-B | 
        #   |   | 
        #   *---D 
        pointA = e.Point(0,0,0)
        pointB = e.Point(0,4,4)
        pointC = e.Point(0,2,2)
        pointD = e.Point(0,6,6)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,0), e.Point(0,2,4)),
                e.Box(e.Point(0,2,0), e.Point(0,4,2)),
                ]

        #    A---* 
        #    |   | 
        #  C-+-* | 
        #  | *-+-B 
        #  |   |   
        #  *---D   


        pointA = e.Point(0,2,0)
        pointB = e.Point(0,6,4)
        pointC = e.Point(0,0,2)
        pointD = e.Point(0,4,6)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,2,0), e.Point(0,4,2)),
                e.Box(e.Point(0,4,0), e.Point(0,6,4)),
                ]

        assert box1 - box2 == expected


        #    C---*
        #    |   |
        #  A-+-* |
        #  | *-+-D
        #  |   |  
        #  *---B  

        pointA = e.Point(0,0,2)
        pointB = e.Point(0,4,6)
        pointC = e.Point(0,2,0)
        pointD = e.Point(0,6,4)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,2), e.Point(0,2,6)),
                e.Box(e.Point(0,2,4), e.Point(0,4,6)),
                ]

        assert box1 - box2 == expected

        #  C---*  
        #  |   |  
        #  | A-+-*
        #  *-+-D |
        #    |   |
        #    *---B

        pointA = e.Point(0,2,2)
        pointB = e.Point(0,6,6)
        pointC = e.Point(0,0,0)
        pointD = e.Point(0,4,4)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,2,4), e.Point(0,4,6)),
                e.Box(e.Point(0,4,2), e.Point(0,6,6)),
                ]

        assert box1 - box2 == expected



    def test_subtraction_inside(self):	
        # Completely inside:
        # C------*  A------*
        # | A-*  |  | C-*  |
        # | | |  |  | | |  |
        # | *-B  |  | *-D  |
        # *------D  *------B
        pointA = e.Point(0,2,2)
        pointB = e.Point(0,4,4)
        pointC = e.Point(0,0,0)
        pointD = e.Point(0,10,10)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        assert box1 - box2 == None

        pointA = e.Point(0,0,0)
        pointB = e.Point(0,10,10)
        pointC = e.Point(0,2,2)
        pointD = e.Point(0,4,4)

        box1 = e.Box(pointA, pointB)
        box2 = e.Box(pointC, pointD)

        expected = [
                e.Box(e.Point(0,0,0), e.Point(0,10,2)),
                e.Box(e.Point(0,0,2), e.Point(0,2,4)),
                e.Box(e.Point(0,4,2), e.Point(0,10,4)),
                e.Box(e.Point(0,0,4), e.Point(0,10,10))
                ]

        assert box1 - box2 == expected
