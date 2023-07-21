from colorama import Fore, Style
import math


class Frange:
    def __init__(self, left, right=None, step=1):
        if right is None:
            left, right = 0, left
        self.left = left
        self.right = right
        self.step = step
        self.comparer = self.left > self.right

    def __next__(self):
        if self.comparer:
            if self.right + self.step >= self.left + self.step or (self.left > 0 and self.right == 0):
                raise StopIteration
            result = self.left
            self.left += self.step if self.step < 0 else -self.step
            return result

        else:
            if self.left + self.step >= self.right + self.step:
                raise StopIteration
            result = self.left
            self.left += self.step
            return result

    def __iter__(self):
        return self

frange = Frange

assert list(frange(5)) == [0, 1, 2, 3, 4]
assert list(frange(2, 5)) == [2, 3, 4]
assert list(frange(2, 10, 2)) == [2, 4, 6, 8]
assert list(frange(10, 2, -2)) == [10, 8, 6, 4]
assert list(frange(2, 5.5, 1.5)) == [2, 3.5, 5]
assert list(frange(1, 5)) == [1, 2, 3, 4]
assert list(frange(0, 5)) == [0, 1, 2, 3, 4]
assert list(frange(0, 0)) == []
assert list(frange(100, 0)) == []

print('SUCCESS!')


class Coloriez:
    def __init__(self, color):
        self.color = color.upper()

    def __enter__(self):
        return getattr(Fore, self.color) + Style.BRIGHT

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Style.RESET_ALL)


with Coloriez('green') as c:
    print(c + "printed in green")

print("print in default color")


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Circle(Shape):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Rectangle):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle

    def print_angle(self):
        print(self.angle)

    def __str__(self):
        result = super().__str__()
        return result + f'\nParallelogram: {self.width}, {self.height}, {self.angle}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def square(self):
        return self.width * self.height * math.sin(math.radians(self.angle))


class Triangle(Shape):
    def __init__(self, x, y, side1, side2, side3):
        super().__init__(x, y)
        self.side_1 = side1
        self.side_2 = side2
        self.side_3 = side3

    def square(self):
        p = (self.side_1 + self.side_2 + self.side_3) / 2
        square = math.sqrt(p * (p - self.side_1) * (p - self.side_2) * (p - self.side_3))
        return square


class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)

    def __str__(self):
        pass


r = Rectangle(0, 0, 10, 20)
r1 = Rectangle(10, 0, -10, 20)
r2 = Rectangle(0, 20, 100, 20)

c = Circle(10, 0, 10)
c1 = Circle(100, 100, 5)

p = Parallelogram(1, 2, 20, 30, 45)
p1 = Parallelogram(1, 2, 20, 30, 45)
str(p1)

t = Triangle(0, 0, 3, 4, 5)
t1 = Triangle(0, 0, 5, 4, 5)

scene = Scene()
scene.add_figure(r)
scene.add_figure(r1)
scene.add_figure(r2)
scene.add_figure(c)
scene.add_figure(c1)
scene.add_figure(t)
scene.add_figure(t1)

scene.total_square()


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
point_inside = Point(2, 2)
point_outside = Point(7, 7)

print(point_inside in circle)
print(point_outside in circle)




