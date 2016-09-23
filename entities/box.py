from point import Point

class Box(object):

    def __init__(self, top_left, bottom_right):
        if type(top_left) != type(Point(0,0,0)):
            raise ValueError("First parameter must be a Point")
        if type(bottom_right) != type(Point(0,0,0)):
            raise ValueError("Second parameter must be a Point")
        self.top_left = top_left
        self.bottom_right = bottom_right

