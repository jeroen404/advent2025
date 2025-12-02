#!/usr/bin/env python3

from math import log10, floor

class IDRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def invalid_ids(self):
        start_nb_digits = floor(log10(self.start)) + 1
        end_nb_digits = floor(log10(self.end)) + 1
        invalids = set()
        for nb_digits in range(start_nb_digits, end_nb_digits + 1):
            if nb_digits % 2 == 0:
                half = nb_digits // 2
                for first_half in range(10**(half - 1), 10**half):
                    invalid_id = first_half * (10**half + 1)
                    if self.start <= invalid_id <= self.end:
                        invalids.add(invalid_id)
        return invalids
    def invalid_ids_part2(self):
        start_nb_digits = floor(log10(self.start)) + 1
        end_nb_digits = floor(log10(self.end)) + 1
        invalids = set()
        for nb_digits in range(start_nb_digits, end_nb_digits + 1):
            for pattern_size in range(1, nb_digits // 2 + 1):
                if nb_digits % pattern_size == 0:
                    for pattern in range(10**(pattern_size - 1), 10**pattern_size):
                        id = pattern
                        for _ in range(2, nb_digits // pattern_size + 1):
                            id = id * (10**pattern_size) + pattern
                        if self.start <= id <= self.end:
                            invalids.add(id)
        return invalids
    def __repr__(self):
        return f"IDRange({self.start} - {self.end})"
    @staticmethod
    def from_string(s):
        start_str, end_str = s.split('-')
        return IDRange(int(start_str), int(end_str))
    
try:
    ranges = [IDRange.from_string(s) for s in input().split(',')]

    part1 = sum(sum(r.invalid_ids()) for r in ranges)
    part2 = sum(sum(r.invalid_ids_part2()) for r in ranges)
    print(part1)
    print(part2)
except EOFError:
    pass