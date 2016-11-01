import copy
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
        self.component_boxes = [self.original_boxes[0]]

        self.add_boxes(self.original_boxes[1:])


    def add_boxes(self, new_boxes):

        for new_box in new_boxes:
            self.add_box(new_box)


    def add_box(self, new_box):

        for old_box in self.component_boxes:
            if new_box.adjecent_to(old_box):
                self.component_boxes.append(new_box)
                return
            if new_box.is_overlapping(old_box):
                new_compound = CompoundBox(old_box) - self
                self += new_compound

    def __add__(self, other):
        raise NotImplementedError("CompoundBox.__add__")

    def __sub__(self, other):
        raise NotImplementedError("CompoundBox.__sub__")

    def __repr__(self):
        for box in self.component_boxes:
            return str(box)


    def _non_overlapping_peices_(self, candidate_box):
        """ Takes a box and returns a list of sub-boxes that don't overlap self"""
        sub_boxes = []
        for existing_box in self.component_boxes:
            if candidate_box.is_overlapping(existing_box):
                overlapping_corners = candidate_box.corners_inside(existing_box)
                num_overlapping_corners = len(overlapping_corners)
                print num_overlapping_corners
                if num_overlapping_corners == 0:
                    raise SystemError('Box claims to be overlapping, but has no corners inside other box')
                if num_overlapping_corners == 1:
                    # Hard case.  Need to chop out a corner
                    overlapping_corner = overlapping_corners[0]
                    if overlapping_corner == candidate_box.top_left:
                        # top chuck
                        new_top_right = Point(0,existing_box.right_edge, candidate_box.top_edge)
                        new_bottom_left = Point(0,candidate_box.right_edge, existing_box.bottom_edge)
                        sub_boxes.append(Box(new_top_right,new_bottom_left))
                        #bottom chunk
                        new_top_left = Point(0,candidate_box.left_edge,existing_box.bottom_edge)
                        sub_boxes.append(Box(new_top_left,candidate_box.bottom_right))
                    elif overlapping_corner == candidate_box.top_right:
                        # top chunk
                        sub_boxes.append(Box(candidate_box.top_left,existing_box.bottom_left))
                        # bottom chunk
                        new_top_left = Point(0,candidate_box.left_edge,existing_box.bottom_edge)
                        sub_boxes.append(Box(new_top_left, candidate_box.bottom_right))
                    elif overlapping_corner == candidate_box.bottom_right:
                        # top chunk
                        new_bottom_right = Point(0,candidate_box.right_edge,existing_box.top_edge)
                        sub_boxes.append(Box(candidate_box.top_left,new_bottom_right))
                        # bottom chunk
                        new_top_left = Point(0,candidate_box.left_edge,existing_box.top_edge)
                        new_bottom_right = Point(0,existing_box.left_edge,candidate_box.bottom_edge)
                        sub_boxes.append(Box(new_top_left, new_bottom_right))
                    elif overlapping_corner == candidate_box.bottom_left:
                        # top chunk
                        new_bottom_right = Point(0,candidate_box.right_edge,existing_box.top_edge)
                        sub_boxes.append(Box(candidate_box.top_left, new_bottom_right))
                        # bottom chunk
                        sub_boxes.append(Box(existing_box.top_left,candidate_box.bottom_right))
                    else:
                        raise NotImplementedError("CompoundBox._non_overlapping_peices_:1:missing_case")
                if num_overlapping_corners == 2:
                    # set the new edge
                    if overlapping_corners[0].x == overlapping_corners[1].x:
                        # vertical line. 
                        print overlapping_corners
                        y = candidate_box.top_edge
                        if candidate_box.left_edge < existing_box.left_edge:
                            x = candidate_box.left_edge
                        else:
                            x = candidate_box.right_edge
                    elif overlapping_corners[0].y == overlapping_corners[1].y:
                        # horizontal line
                        x = candidate_box.left_edge
                        if candidate_box.bottom_edge > existing_box.bottom_edge:
                            y = existing_box.bottom_edge
                        else:
                            y = existing_box.top_edge
                        new_box = Box(Point(0,x,y), candidate_box.bottom_right)
                        sub_boxes.append(new_box)
                    else:
                        raise SystemError('Box claims to have 2 corners overlapping, but y!=y and x!=x')
                if num_overlapping_corners == 3:
                    print overlapping_corners
                    raise NotImplementedError("CompoundBox._non_overlapping_peices_:2")
                    # return the corner that's left
                if num_overlapping_corners == 4:
                    # It's completely inside this box.
                    return None # If this causes issues, return [] instead.
            else:
                print "not overlapping"
                return candidate_box
        return sub_boxes
