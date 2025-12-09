#!/usr/bin/env python3


class Point2D:    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    def area_with(self, other) -> int:
        width = abs(self.x - other.x) + 1 # fat lines
        height = abs(self.y - other.y) + 1
        return width * height
    def inside_polygon(self, polygon: list['Point2D']) -> bool:
        # ray-casting algorithm
        # defitely not stolen 
        # not needed for my input but makes it correct for conclave polygons
        n = len(polygon)
        inside = False
        x = self.x
        y = self.y
        p1x = polygon[0].x
        p1y = polygon[0].y
        for i in range(n + 1):
            p2x = polygon[i % n].x
            p2y = polygon[i % n].y
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    def __eq__(self, other) -> bool:
        return (self.x == other.x) and (self.y == other.y)
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"
    @staticmethod
    def from_string(s: str):
        x_str, y_str = s.strip().split(',')
        return Point2D(int(x_str), int(y_str))
    
class Line2D:
    def __init__(self, p1: Point2D, p2: Point2D):
        self.p1 = p1
        self.p2 = p2
        self.min_x = min(p1.x, p2.x)
        self.max_x = max(p1.x, p2.x)
        self.min_y = min(p1.y, p2.y)
        self.max_y = max(p1.y, p2.y)
    def length(self) -> float:
        return ((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2) ** 0.5
    def has_point_inside(self, rectangle) -> bool:
        return not (self.max_x <= rectangle.bottom_left.x or
                    self.min_x >= rectangle.top_right.x or
                    self.max_y <= rectangle.bottom_left.y or
                    self.min_y >= rectangle.top_right.y)
    def __repr__(self) -> str:
        return f"Line2D({self.p1}, {self.p2})"

class Rectangle2D:
    def __init__(self, bottom_left: Point2D, top_right: Point2D):
        self.bottom_left = Point2D(min(bottom_left.x, top_right.x), min(bottom_left.y, top_right.y))
        self.top_right = Point2D(max(bottom_left.x, top_right.x), max(bottom_left.y, top_right.y))
    def area(self) -> int:
        width = abs(self.top_right.x - self.bottom_left.x) + 1  # fat lines
        height = abs(self.top_right.y - self.bottom_left.y) + 1
        return width * height
    def center(self) -> Point2D:
        cx = (self.bottom_left.x + self.top_right.x) // 2
        cy = (self.bottom_left.y + self.top_right.y) // 2
        return Point2D(cx, cy)
    def __repr__(self) -> str:
        return f"Rectangle2D({self.bottom_left}, {self.top_right})"

points = []

try:
    while True:
        line = input()
        point = Point2D.from_string(line)
        points.append(point)
except EOFError:
    pass

# part 1
largest_area = 0
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        area = points[i].area_with(points[j])
        if area > largest_area:
            largest_area = area

print(largest_area)

# part 2
lines = []
for i, point in enumerate(points[:-1]):
    line = Line2D(point, points[i+1])
    lines.append(line)
lines.append(Line2D(points[-1], points[0]))

# sort lines by length descending
# makes them intersect faster
lines.sort(key=lambda l: l.length(), reverse=True)

largest_area = 0

for i in range(len(points)):
    for j in range(i + 1, len(points)):
        rectangle = Rectangle2D(points[i], points[j])

        area = rectangle.area()
        if area <= largest_area:
            continue
        # Check if rectangle center is inside the polygon
        # not needed for input but otherwise conclave polygons could cause issues
        # makes it take twice as long though..
        if not rectangle.center().inside_polygon(points):
            continue
        intersects = False
        for line in lines:
            if line.has_point_inside(rectangle):
                intersects = True
                break
        if not intersects:
            if area > largest_area:
                largest_area = area
print(largest_area)
