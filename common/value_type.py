import math

from attr import attrib, attrs


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        else:
            return Point(self.x * other, self.y * other)
    
    def __xor__(self, other):
        return self.x * other.y - self.y * other.x
    
    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
    
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        ret = Point(self.x, self.y)
        ret.normalize_()
        return ret
    
    def normalize_(self):
        length = self.length()
        length = max(length, 1e-10)
        self.x /= length
        self.y /= length


class Sample(object):
    def __init__(self, x: float = 0, y: float = 0, tag: int = 0):
        self.point = Point(x, y)
        self.tag = tag
    
    def __str__(self):
        return '[{}: {}]'.format(str(self.point), self.tag)


class Line(object):
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
    
    def __str__(self):
        return '(a={}, b={}, c={})'.format(self.a, self.b, self.c)
    
    def is_valid(self):
        return self.a != 0 or self.b != 0


if __name__ == '__main__':
    test_1 = Point(2, 2)
    test_2 = Point(1, 3)
    print((test_1 - test_2) ^ Point(1, 1))

    test_nor = Point(3, 4)
    test_nor.normalize_()
    print(test_nor)

    test_nor = Point(3, 4)
    print(test_nor.normalize())
    print(test_nor)
