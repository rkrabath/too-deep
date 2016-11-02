import copy
from box import Box
from point import Point
class CompoundBox(object):
    global DEBUG
    DEBUG = False

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
                new_parts = self._non_overlapping_peices_(new_box)
                self.component_boxes.extend(new_parts)

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


    def overlaps_box(self, box):
        for existing_box in self.component_boxes:
            if box.is_overlapping(existing_box):
                return True
        return False


    def _non_overlapping_peices_(self, candidate_box, iteration=0):
        """ Takes a box and returns a list of sub-boxes that don't overlap self"""
        if iteration > 2:
            raise SystemError('More than 10 iterations while trying to find non-overlapping boxes')

        if not self.overlaps_box(candidate_box):
            return [candidate_box]

        for existing_box in self.component_boxes:
            if DEBUG: print "checking " + str(candidate_box) + " against " + str(existing_box)
            overlapping_corners = candidate_box.corners_inside(existing_box)
            num_overlapping_corners = len(overlapping_corners)
            if num_overlapping_corners == 0:
                continue
                #print '======='
                #print existing_box
                #print candidate_box
                #print '======='
                #raise SystemError('Box claims to be overlapping, but has no corners inside other box')
            if num_overlapping_corners == 1:
                sub_boxes = self._cut_out_one_corner_(candidate_box, overlapping_corners[0], existing_box)
                break
            if num_overlapping_corners == 2:
                sub_boxes = self._cut_out_two_corners_(candidate_box, overlapping_corners, existing_box)
                break
            if num_overlapping_corners == 3:
                print overlapping_corners
                raise NotImplementedError("CompoundBox._non_overlapping_peices_:2")
                # return the corner that's left
            if num_overlapping_corners == 4:
                # It's completely inside this box.
                return None # If this causes issues, return [] instead.
                
        filtered_boxes = []
        for box in sub_boxes:
            if box.top_edge == box.bottom_edge or box.right_edge == box.left_edge:
                if DEBUG: print "box {0} has zero area.  discarding".format(box)
                continue
            filtered_boxes.extend(self._non_overlapping_peices_(box, iteration=iteration+1))

        return filtered_boxes

        # Verify that none of the sub-boxes are overlapping anything:
        # iterations = 0
        # while True:
        #     new_sub_boxes = []
        #     for new_box in sub_boxes:
        #         for existing_box in self.component_boxes:
        #             if new_box.is_overlapping(existing_box):
        #                new_sub_boxes.extend(self._non_overlapping_peices_(new_box))
        #             else:
        #                 new_sub_boxes.append(new_box)

        #     print new_sub_boxes
        #     print sub_boxes
        #     if new_sub_boxes == sub_boxes:
        #         return sub_boxes

        #     sub_boxes = new_sub_boxes
        #     if iterations > 1:
        #         raise SystemError('More than 10 iterations while trying to find non-overlapping boxes')
        #     iterations += 1


    def _cut_out_one_corner_(self, candidate_box, overlapping_corner, existing_box):
        # Hard case.  Need to chop out a corner
        sub_boxes = []
        if overlapping_corner == candidate_box.top_left:
            if DEBUG: print "Cutting out top left chunk of " + str(candidate_box)
            # top chuck
            new_top_right = Point(0,existing_box.right_edge, candidate_box.top_edge)
            new_bottom_left = Point(0,candidate_box.right_edge, existing_box.bottom_edge)
            sub_boxes.append(Box(new_top_right,new_bottom_left))
            #bottom chunk
            new_top_left = Point(0,candidate_box.left_edge,existing_box.bottom_edge)
            sub_boxes.append(Box(new_top_left,candidate_box.bottom_right))
        elif overlapping_corner == candidate_box.top_right:
            if DEBUG:  print "Cutting out top left right"
            # top chunk
            sub_boxes.append(Box(candidate_box.top_left,existing_box.bottom_left))
            # bottom chunk
            new_top_left = Point(0,candidate_box.left_edge,existing_box.bottom_edge)
            sub_boxes.append(Box(new_top_left, candidate_box.bottom_right))
        elif overlapping_corner == candidate_box.bottom_right:
            if DEBUG: print "Cutting out bottom right chunk"
            # top chunk
            new_bottom_right = Point(0,candidate_box.right_edge,existing_box.top_edge)
            sub_boxes.append(Box(candidate_box.top_left,new_bottom_right))
            # bottom chunk
            new_top_left = Point(0,candidate_box.left_edge,existing_box.top_edge)
            new_bottom_right = Point(0,existing_box.left_edge,candidate_box.bottom_edge)
            sub_boxes.append(Box(new_top_left, new_bottom_right))
        elif overlapping_corner == candidate_box.bottom_left:
            if DEBUG: print "Cutting out bottom left chunk of " + str(candidate_box)
            # top chunk
            new_bottom_right = Point(0,candidate_box.right_edge,existing_box.top_edge)
            sub_boxes.append(Box(candidate_box.top_left, new_bottom_right))
            # bottom chunk
            sub_boxes.append(Box(existing_box.top_right,candidate_box.bottom_right))
        else:
            raise NotImplementedError("CompoundBox._non_overlapping_peices_:1:missing_case")
        return sub_boxes


    def _cut_out_two_corners_(self, candidate_box, overlapping_corners, existing_box):
        # set the new edge
        if overlapping_corners[0].x == overlapping_corners[1].x:
            # vertical line. 
            y = candidate_box.top_edge
            if candidate_box.left_edge < existing_box.left_edge:
                if DEBUG: print "chopping off right side"
                x = candidate_box.left_edge
            else:
                if DEBUG: print "chopping off left side"
                x = candidate_box.right_edge
            new_box = Box(Point(0,x,y), candidate_box.bottom_right)
        elif overlapping_corners[0].y == overlapping_corners[1].y:
            # horizontal line
            x = candidate_box.left_edge
            if candidate_box.bottom_edge > existing_box.bottom_edge:
                if DEBUG: print "chopping off top edge of " + str(candidate_box)
                y = existing_box.bottom_edge
            else:
                if DEBUG: print "chopping off bottom edge of " + str(candidate_box)
                y = existing_box.top_edge
            new_box = Box(Point(0,x,y), candidate_box.bottom_right)
            if DEBUG: print "left with " + str(new_box)
        else:
            raise SystemError('Box claims to have 2 corners overlapping, but y!=y and x!=x')
        return [new_box]
