from point import Point

class Box(object):

    def __init__(self, top_left, bottom_right):
        if type(top_left) != type(Point(0,0,0)):
            raise ValueError("First parameter must be a Point")
        if type(bottom_right) != type(Point(0,0,0)):
            raise ValueError("Second parameter must be a Point")

        self.top_left = top_left
        self.bottom_right = bottom_right

        self.top_right = Point(0,self.bottom_right.x, self.top_left.y)
        self.bottom_left = Point(0,self.top_left.x, self.bottom_right.y)

        self.left_edge = self.top_left.x
        self.right_edge = self.bottom_right.x
        self.top_edge = self.top_left.y
        self.bottom_edge = self.bottom_right.y


    def adjecent_to(self, other):
        if self.left_edge == other.right_edge:
            return True
        if self.right_edge == other.left_edge:
            return True
        if self.top_edge == other.bottom_edge:
            return True
        if self.bottom_edge == other.top_edge:
            return True

        return False



    def is_overlapping(self, other, reverse=True):
        # If any of the points of other are inside self, then we're overlapping.
        for candidate_corner in other.corners:
            x, y = candidate_corner.xy()
            if self.left_edge < x < self.right_edge:
                if self.top_edge < y < self.bottom_edge:
                    return True

        # Sometimes the opposite might be true instead:
        if reverse and other.is_overlapping(self, reverse=False):
            return True

        # Sometimes the boxes might cross but not actually have points inside each other
        #
        #     +--+
        #     |O |
        # +---|--|---+
        # | S |  |   |
        # +---|--|---+
        #     |  |
        #     +--+

        if self.left_edge < other.right_edge < self.right_edge:
            if other.top_edge < self.top_edge < other.bottom_edge:
                return True

        # Still overlapping:
        # A--*
        # |S |
        # C--+-*
        # |  |O|
        # *--+-D
        # |  |
        # *--B
        # Because even though C is not inside Box(A,B), C is on the opposite side of it than D
        if self.left_edge == other.left_edge:
            if other.right_edge > self.left_edge:
                return True
        if self.right_edge == other.right_edge:
            if other.left_edge < self.right_edge:
                return True
        if self.top_edge == other.top_edge:
            if other.bottom_edge > self.top_edge:
                return True
        if self.bottom_edge == other.bottom_edge:
            if other.top_edge < self.bottom_edge:
                return True
               
        return False


    def corners_inside(self, other):
        corners = []
        for corner in self.corners:
            if corner.inside(other):
                corners.append(corner)

        # The point might not be inside, instead just touching, but still the box is overlapping
        if self.left_edge == other.left_edge:
            if other.right_edge > self.left_edge:
                corners.append(self.top_left)
                corners.append(self.bottom_left)
        if self.right_edge == other.right_edge:
            if other.left_edge < self.right_edge:
                corners.append(self.top_right)
                corners.append(self.bottom_right)
        if self.top_edge == other.top_edge:
            if other.bottom_edge > self.top_edge:
                corners.append(self.top_right)
                corners.append(self.top_left)
        if self.bottom_edge == other.bottom_edge:
            if other.top_edge < self.bottom_edge:
                corners.append(self.bottom_right)
                corners.append(self.bottom_left)

        return corners

    @property
    def corners(self):
        return [
                self.top_left,
                self.top_right,
                self.bottom_left,
                self.bottom_right
                ]

    def __repr__(self):
        return str((self.top_left, self.bottom_right))


    def __eq__(self, other):
        if self.top_left == other.top_left:
            if self.bottom_right == other.bottom_right:
                return True
        return False


    def __sub__(self, other):

        # Sometimes the boxes might cross but not actually have points inside each other
        #
        #     +--+           +--+     
        #     |O |           |S |     
        # +---|--|---+   +---|--|---+ 
        # | S |  |   |   | O |  |   | 
        # +---|--|---+   +---|--|---+ 
        #     |  |           |  |     
        #     +--+           +--+     

        if self.left_edge < other.left_edge < other.right_edge < self.right_edge:
            if other.top_edge < self.top_edge < self.bottom_edge < other.bottom_edge:
                return self._cut_out_middle(other.left_edge, other.right_edge, axis='x')

        if self.top_edge < other.top_edge < other.bottom_edge < self.bottom_edge:
            if other.left_edge < self.left_edge < self.right_edge < other.right_edge:
                return self._cut_out_middle(other.left_edge, other.right_edge, axis='y')


        # Still overlapping:
        # A--*      A---C---*--*
        # |S |      | S |   |  |
        # C--+-*    *---+---+--B
        # |  |O|        |   |
        # *--+-D        | O |
        # |  |          *---D
        # *--B
        # Because even though C is not inside Box(A,B), C is on the opposite side of it than D
        if self.left_edge == other.left_edge:
            if other.right_edge > self.left_edge:
                return self._cut_out_middle(other.top_edge, other.bottom_edge, 'y')
        if self.right_edge == other.right_edge:
            if other.left_edge < self.right_edge:
                return self._cut_out_middle(other.top_edge, other.bottom_edge, 'y')
        if self.top_edge == other.top_edge:
            if other.bottom_edge > self.top_edge:
                return self._cut_out_middle(other.left_edge, other.right_edge, 'x')
        if self.bottom_edge == other.bottom_edge:
            if other.top_edge < self.bottom_edge:
                return self._cut_out_middle(other.left_edge, other.right_edge, 'x')


        # Two points inside:
        # A----*       A----*   A-----*            
        # |    |       |    |   |     |     C-*    
        # |  C-+-*   C-+-*  |   | C-* |     | |    
        # |  | | |   | | |  |   *-+-+-B   A-+-+-*  
        # |  *-+-D   *-+-D  |     | |     | *-D |  
        # |    |       |    |     *-D     |     |  
        # *----B       *----B             *-----B  
        if self.top_edge < other.top_edge < other.bottom_edge < self.bottom_edge:
            if self.left_edge < other.left_edge < self.right_edge < other.right_edge:
                boxes = self._cut_out_middle(other.top_edge, other.bottom_edge, 'y')
                point_a = Point(0,self.left_edge, other.top_edge)
                point_b = Point(0,other.left_edge, other.bottom_edge)
                boxes.append(Box(point_a, point_b))
                return boxes
            if other.left_edge < self.left_edge < other.right_edge < self.right_edge:
                boxes = self._cut_out_middle(other.top_edge, other.bottom_edge, 'y')
                point_a = Point(0,other.left_edge, other.top_edge)
                point_b = Point(0,self.right_edge, other.bottom_edge)
                boxes.append(Box(point_a, point_b))
                return boxes
        if self.left_edge < other.left_edge < other.right_edge < self.right_edge:
            if self.top_edge < other.top_edge < self.bottom_edge < other.bottom_edge:
                boxes = self._cut_out_middle(other.left_edge, other.right_edge, 'x')
                point_a = Point(0,other.left_edge, self.top_edge)
                point_b = Point(0,other.right_edge, self.top_edge)
                boxes.append(Box(point_a, point_b))
                return boxes
            if other.top_edge < self.top_edge < other.bottom_edge < self.bottom_edge:
                boxes = self._cut_out_middle(other.left_edge, other.right_edge, 'x')
                point_a = Point(0,other.left_edge, other.bottom_edge)
                point_b = Point(0,other.right_edge, self.bottom_edge)
                boxes.append(Box(point_a, point_b))
                return boxes


        # One point inside:
        # A---*      A---*    C---*  C---*  
        # |   |      |   |    |   |  |   |  
        # | C-+-*  C-+-* |  A-+-* |  | A-+-*
        # *-+-B |  | *-+-B  | *-+-D  *-+-D |
        #   |   |  |   |    |   |      |   |
        #   *---D  *---D    *---B      *---B
        if self.top_edge < other.top_edge < self.bottom_edge < other.bottom_edge:
            if self.left_edge < other.left_edge < self.right_edge < other.right_edge:
                box_1_a = self.top_left
                box_1_b = Point(0,other.left_edge, self.bottom_edge)
                box_2_a = Point(0,other.left_edge, self.top_edge)
                box_2_b = Point(0,self.right_edge, other.top_edge)
                box1 = Box(box_1_a, box_1_b)
                box2 = Box(box_2_a, box_2_b)
                return [box1, box2]
            if other.left_edge < self.left_edge < other.right_edge < self.right_edge:
                box_1_a = self.top_left
                box_1_b = other.top_right
                box_2_a = Point(other.right_edge, self.top_edge)
                box_2_b = self.bottom_right
                box1 = Box(box_1_a, box_1_b)
                box2 = Box(box_2_a, box_2_b)
                return [box1, box2]
        if other.top_edge < self.top_edge < other.bottom_edge < self.bottom_edge:
            if self.left_edge < other.left_edge < self.right_edge < other.right_edge:
                box_1_a = self.top_left
                box_1_b = Point(other.left_edge, self.bottom_edge)
                box_2_a = other.bottom_left
                box_2_b = self.bottom_right
                box1 = Box(box_1_a, box_1_b)
                box2 = Box(box_2_a, box_2_b)
                return [box1, box2]
            if other.left_edge < self.left_edge < other.right_edge < self.right_edge:
                box_1_a = Point(0,self.left_edge, other.bottom_edge)
                box_1_b = Point(0,other.right_edge, self.bottom_edge)
                box_2_a = Point(0,other.right_edge, self.tom_edge)
                box_2_b = self.bottom_right
                box1 = Box(box_1_a, box_1_b)
                box2 = Box(box_2_a, box_2_b)
                return [box1, box2]


        # Completely inside:
        # A------*  C------*
        # | C-*  |  | A-*  |
        # | | |  |  | | |  |
        # | *-D  |  | *-B  |
        # *------B  *------D
        if self.top_edge < other.top_edge < other.bottom_edge < self.bottom_edge:
            if self.left_edge < other.left_edge < other.right_edge < self.right_edge:
                # cut a hole.  return 4 boxes.
                point_a_1 = self.top_left
                point_b_1 = Point(0,self.right_edge, other.top_edge)
                point_a_2 = Point(0,self.left_edge, other.top_edge)
                point_b_2 = other.bottom_left
                point_a_3 = other.top_right
                point_b_3 = Point(0,self.right_edge, other.bottom_edge)
                point_a_4 = Point(0,self.left_edge, other.bottom_edge)
                point_b_4 = self.bottom_right
                return [
                    Box(point_a_1, point_b_1),
                    Box(point_a_2, point_b_2),
                    Box(point_a_3, point_b_3),
                    Box(point_a_4, point_b_4)
                    ]


        if other.top_edge < self.top_edge < self.bottom_edge < other.bottom_edge:
            if other.left_edge < self.left_edge < self.right_edge < other.right_edge:
                return None



    def _cut_out_middle(first_border, second_border, axis):
        """ If axis is 'x', resultant boxes will be "next to" eachother.  If 
        it's 'y', they will be "on top" of each other"""
        chunks = []

        if axis == 'x':
            one_point_b_x = first_border
            one_point_b_y = self.bottom_edge
            two_point_a_x = second_border
            two_point_a_y = self.top_edge
        else:
            one_point_b_x = self.left_edge
            one_point_b_y = first_border
            two_point_a_x = self.left_edge
            two_point_a_y = second_border
        one_point_a = self.top_left
        one_point_b = Point(0, one_point_b_x, one_point_b_y)
        two_point_b = Point(0, two_point_b_x, two_point_b_y)
        two_point_b = self.bottom_right

        chunks.append(Box(one_point_a, one_point_b))
        chunks.append(Box(two_point_a, two_point_b))

        return chunks
