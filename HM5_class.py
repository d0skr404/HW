import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle(Point):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def __contains__(self, point):
        distance = math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
        return distance <= self.radius


circle = Circle(0, 0, 5)
point1 = Point(3, 3)
point2 = Point(6, 6)

print(point1 in circle)  # True, точка (3, 3) знаходиться в колі
print(point2 in circle)  # False, точка (6, 6) знаходиться поза колом
