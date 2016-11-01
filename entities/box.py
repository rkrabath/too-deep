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


        return False


    def corners_inside(self, other):
        corners = []
        for corner in self.corners:
            if corner.inside(other):
                corners.append(corner)
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
