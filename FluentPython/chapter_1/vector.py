
from math import hypot


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(self.x or self.y)

    def __add__(self, other):
        x = self.x + other
        y = self.y + other
        return Vector(x, y)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

if __name__ == "__main__":
    v = Vector(3, 4)
    print(v)
    print(abs(v))
    print(v * 5)
    print(5 * v)
    print(v + 5)
    print(5 + v)
