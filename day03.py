#!/usr/bin/env python3

from functools import cache


def part1_max(capacities):
    max1 = 0
    max2 = 0
    for i in range(len(capacities)-1):
        if capacities[i] > max1:
            max1 = capacities[i]
            max2 = 0
            for j in range(i+1, len(capacities)):
                if capacities[j] > max2:
                    max2 = capacities[j]
    return max1 * 10 + max2

@cache
def part2_max(capacities,remaining_batteries) -> int:
    if remaining_batteries == 1:
        return max(capacities)
    bank_len = len(capacities)
    max_so_far = 0
    last_possible_start = bank_len - remaining_batteries + 1
    biggest_start = max(capacities[0:last_possible_start])
    for start_pos in range(0,last_possible_start):
        if capacities[start_pos] == biggest_start:
            next_max = part2_max(capacities[start_pos+1:], remaining_batteries-1)
            if next_max > max_so_far:
                max_so_far = next_max
    return biggest_start * (10 ** (remaining_batteries - 1)) + max_so_far

banks = []
try:
    while True:
        line = input()
        banks.append([int(c) for c in line.strip()])
        if not line:
            break
    
except EOFError:
    pass


total_part1 = sum(part1_max(bank) for bank in banks)
total_part2 = sum(part2_max(tuple(bank), 12) for bank in banks)
print(total_part1)
print(total_part2)