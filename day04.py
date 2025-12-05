#!/usr/bin/env python3

class Point:
    def __init__(self, x=0, y=0, type_char=''):
        self.x = x
        self.y = y
        self.type_char = type_char

class Grid:
    def __init__(self):
        self.points = []
        self.max_x = 0
        self.max_y = 0
    def add_row(self, line):
        row = [Point(x=i, y=len(self.points), type_char=ch) for i, ch in enumerate(line)]
        self.points.append(row)
        self.max_x = max(self.max_x, len(row))
        self.max_y = len(self.points)
    def get_point(self, x, y):
        return self.points[y][x]
    def display(self):
        for row in self.points:
            print(''.join(p.type_char for p in row))
    #diagonal included        
    def neighbors(self, point):
        neighbors = []
        x, y = point.x, point.y
        if x > 0:
            neighbors.append(self.get_point(x - 1, y))
            if y > 0:
                neighbors.append(self.get_point(x - 1, y - 1))
            if y < self.max_y - 1:
                neighbors.append(self.get_point(x - 1, y + 1))
        if x < self.max_x - 1:
            neighbors.append(self.get_point(x + 1, y))
            if y > 0:
                neighbors.append(self.get_point(x + 1, y - 1))
            if y < self.max_y - 1:
                neighbors.append(self.get_point(x + 1, y + 1))
        if y > 0:
            neighbors.append(self.get_point(x, y - 1))
        if y < self.max_y - 1:
            neighbors.append(self.get_point(x, y + 1))
        return neighbors
    def iter_points(self):
        for row in self.points:
            for point in row:
                yield point
    def iter_type(self, type_char):
        for point in self.iter_points():
            if point.type_char == type_char:
                yield point
    def replace_type(self, old_type, new_type):
        for point in self.iter_type(old_type):
            point.type_char = new_type

try:
    grid = Grid()
    while True:
        line = input().strip()
        if not line:
            break
        grid.add_row(line)
except EOFError:
    pass    

found = True
part1_first_loop = True
foundnb = 0
while found:
    found = False
    for point in grid.iter_type('@'):
        if len([n for n in grid.neighbors(point) if n.type_char != '.'] ) < 4 :
            point.type_char = 'x'
            found = True
            foundnb += 1
    if part1_first_loop:
        part1_first_loop = False
        print(foundnb)
    grid.replace_type('x', '.')

print(foundnb)