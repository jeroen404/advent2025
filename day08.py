#!/usr/bin/env python3

from math import sqrt
import heapq

class Point3D:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
    def euclidean_distance(self, other) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
    def __eq__(self, other) -> bool:
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    def __repr__(self) -> str:
        return f"Point3D({self.x}, {self.y}, {self.z})"
    @staticmethod
    def from_string(s: str):
        x_str, y_str, z_str = s.strip().split(',')
        return Point3D(int(x_str), int(y_str), int(z_str))
    

circuits: list[set[Point3D]] = []
points = []

try:
    while True:
        line = input()
        point = Point3D.from_string(line)
        # each point starts a new circuit
        circuits.append({point})
        points.append(point)
except EOFError:
    pass

distances = {}
pq = []

# mr robot gave a hint to use a priority queue
print("Precomputing distances...")
for i in range(len(circuits)-1):
    for j in range(i+1, len(circuits)):
        shortest_distance = int(1e12)
        for point1 in circuits[i]:
            for point2 in circuits[j]:
                dist = point1.euclidean_distance(point2)
                if dist < shortest_distance:
                    shortest_distance = dist
        distances[(i, j)] = shortest_distance
        heapq.heappush(pq, (shortest_distance, i, j))


def place_a_wire():
    #global circuits, distances, pq, points
    dist, i, j = heapq.heappop(pq)
    # check if they are in the same circuit
    circuit_i = None
    circuit_j = None
    p1 = points[i]
    p2 = points[j]
    for index, circuit in enumerate(circuits):
        if p1 in circuit:
            circuit_i = index
        if p2 in circuit:
            circuit_j = index
    if circuit_i is not None and circuit_j is not None and circuit_i != circuit_j:
        # merge circuits
        circuits[circuit_i].update(circuits[circuit_j])
        del circuits[circuit_j]
    return (p1, p2)

nb_of_wires = 1000
for _ in range(nb_of_wires):
    place_a_wire()

print(len(circuits))

circuit_lengths = [len(circuit) for circuit in circuits]
#get three largest
circuit_lengths.sort(reverse=True)
part1_result = circuit_lengths[0] * circuit_lengths[1] * circuit_lengths[2]
print(part1_result)


# part 2
while len(circuits) > 1:
    p1, p2 = place_a_wire()

print(p1.x * p2.x)

