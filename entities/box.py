from point import Point

class Box(object):

    def __init__(self, top_left, bottom_right):
        if type(top_left) != type(Point(0,0,0)):
            raise ValueError("First parameter must be a Point")
        if type(bottom_right) != type(Point(0,0,0)):
            raise ValueError("Second parameter must be a Point")

        self.top_left = top_left
        self.bottom_right = bottom_right

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


    def is_overlapping(self, other):
        updown = False
        leftright = False
        if self.left_edge < other.left_edge < self.right_edge:
            leftright = True
        if self.right_edge > other.right_edge > self.left_edge:
            leftright = True
        if self.top_edge < other.top_edge < self.bottom_edge:
            updown = True
        if self.bottom_edge > other.bottom_edge > self.top_edge:
            updown = True

        return updown and leftright
