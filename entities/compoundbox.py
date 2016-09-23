from box import Box
from point import Point
class CompoundBox(object):

    def __init__(self, potentially_many_boxes):
        if type(potentially_many_boxes) != type([]):
            boxes = [potentially_many_boxes]
        else:
            boxes = potentially_many_boxes

        for box in boxes:
            if type(box) != type(Box(Point(0,4,4),Point(0,4,4))):
                raise ValueError("All input points must be wrapped in a Box")

        self.original_boxes = boxes	

