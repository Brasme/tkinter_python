import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @staticmethod
    def from_tuple(xy):
        return Point(xy[0],xy[1])        
    
    def __str__(self):
        return f"Point({self.x},{self.y})"
    
    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def distance(self,other):
        return (self-other).length()


p = Point(1,2)
print(p)

p = p + Point(2,2)
print(p)

print(Point.from_tuple([5,6]))
print(Point.from_tuple((5,7)))

print(p.length())

print(Point(5,6).distance(Point(7,-11)))