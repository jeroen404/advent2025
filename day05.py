#!/usr/bin/env python3

class FreshRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    @staticmethod
    def from_string(s):
        start_str, end_str = s.split('-')
        return FreshRange(int(start_str), int(end_str))
    def in_range(self, value):
        return self.start <= value <= self.end
    def overlaps(self, other):
        return not (self.end < other.start or other.end < self.start)
    def merge(self, other: 'FreshRange'):    
        self.start = min(self.start, other.start)
        self.end =  max(self.end, other.end)
    def length(self):
        return self.end - self.start + 1
    

ranges = set()
values = []
try:
    while True:
        line = input().strip()
        if not line:
            break
        if line == "":
            break
        ranges.add(FreshRange.from_string(line))
    while True:
        line = input().strip()
        if not line:
            break
        values.append(int(line))
except EOFError:
    pass

# part 1
print (len([v for v in values if any(r.in_range(v) for r in ranges)]))

# part 2
found_overlap = True
while found_overlap:
    found_overlap = False
    new_ranges = set()
    used = set()
    for r1 in ranges:
        if r1 in used:
            continue
        # maybe an array would have been better than a set ...
        for r2 in ranges:
            if r1 != r2 and r2 not in used and r1.overlaps(r2):
                r1.merge(r2)
                used.add(r2)
                found_overlap = True
        new_ranges.add(r1)
    ranges = new_ranges

total_length = sum(r.length() for r in ranges)
print(total_length)