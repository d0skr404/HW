import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle(Point):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def contains(self, point):
        distance = math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
        return distance <= self.radius


circle = Circle(0, 0, 5)
point_inside = Point(2, 2)
point_outside = Point(7, 7)

print(circle.contains(point_inside))  # Виведе True
print(circle.contains(point_outside))  # Виведе False
