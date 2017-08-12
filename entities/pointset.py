from point import Point

class Pointset(object):

    def __init__(self, points=None):
        self.points = set()

        if points:
            self.points.update([self.coerce(x) for x in points])
                

    def __add__(self, other):
        if type(other) is Pointset:
            self.points.update(other)
            return self
        if type(other) is Point:
            self.points.add(other)
            return self
        raise TypeError("Can't add "+type(other)+" to Pointset")


    def __iadd__(self, other):
        return self.__add__(other)


    def __sub__(self, other):
        if type(other) is Pointset:
            self.points = self.points - other.points
            return self
        if type(other) is Point:
            self.discard(other)
            return self
        raise TypeError("Can't remove "+type(other)+" from Pointset")
         
    
    def __iter__(self):
        return (point for point in self.points)
        

    def __repr__(self):
        return str(self.points) 

    def coerce(self, possible_point):
        if type(possible_point) is Point:
            return possible_point
        else:
            return Point(*possible_point)
        
