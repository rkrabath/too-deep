import sys
import copy
from box import Box
from point import Point
class CompoundBox(object):
    global DEBUG
    DEBUG = False

    def __init__(self, potentially_many_boxes):
        if not potentially_many_boxes:
            self.original_boxes = None
            self.component_boxes = []
            return

        if type(potentially_many_boxes) != type([]):
            boxes = [potentially_many_boxes]
        else:
            boxes = potentially_many_boxes

        for box in boxes:
            if type(box) != type(Box(Point(0,4,4),Point(0,4,4))):
                raise ValueError("All input points must be wrapped in a Box")

        self.original_boxes = boxes	
        self.component_boxes = [self.original_boxes[0]]

        self.add_boxes(self.original_boxes[1:])


    def add_boxes(self, new_boxes):

        for new_box in new_boxes:
            self.add_box(new_box)


    def add_box(self, new_box):
        sys.setrecursionlimit(15)
        if not self.component_boxes:
            self.component_boxes = [new_box]
            return

        for existing_box in self.component_boxes:
            sub_boxes = new_box - existing_box
            for sub in sub_boxes:
                if sub.top_left == sub.bottom_right:
                    raise ValueError('found it')
            if len(sub_boxes) == 0:
                return # Box was totaly inside an existing box
            if len(sub_boxes) > 1:
                self.add_boxes(sub_boxes) # New box was partially inside this box, so
                return                    # check just the parts that weren't overlapping.
            if len(sub_boxes) == 1 and sub_boxes[0] != new_box:
                self.add_box(sub_boxes[0])  # New box was partially inside an existing one, and
                return  # we got one part back that wasn't.  Check it agains the rest of the boxes.
            if sub_boxes[0] == new_box:
                continue # This box doesn't overlap with this existing box.  Check the next one.
            raise NotImplemented("It should be impossible to get here.")

        # If we've gotten here then this box doesn't overlap any of the exsiting boxes
        self.component_boxes.append(new_box)


    def __add__(self, other):
        for box in other.component_boxes:
            new_peices = self._non_overlapping_peices_(box)
            self.component_boxes.extend(new_peices)
        #raise NotImplementedError("CompoundBox.__add__")


    def __sub__(self, other):
        remaining_peices = []
        for component_box in self.component_boxes:
            remaining_boxes = other._non_overlapping_peices_(component_box)
            remaining_peices.extend(other._non_overlapping_peices_(component_box))
        return CompoundBox(remaining_peices)
        #raise NotImplementedError("CompoundBox.__sub__")


    def __repr__(self):
        return str(self.component_boxes)


