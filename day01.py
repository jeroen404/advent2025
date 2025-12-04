#!/usr/bin/env python3

instructions = []
directions_map = { 'L': -1, 'R': 1 }
try:
    while True:
        line = input().strip()
        if not line:
            break
        direction = line[0]
        distance = int(line[1:])
        instruction = directions_map[direction] * distance
        instructions.append(instruction)
except EOFError:
    pass

pos = 50
end_zeros = 0
zeros = 0

for instruction in instructions:

    new_pos = pos + instruction

    if new_pos % 100 == 0:
        end_zeros += 1
    if instruction > 0:
        zeros += new_pos // 100
    elif instruction < 0:
        # Calculate crossings by comparing the integer block of start and end
        # We shift by -1 to handle the 0 boundary correctly for negative moves
        # It comes from AI .. and somehow it works
        zeros += (pos - 1) // 100 - (new_pos - 1) // 100

    pos = new_pos % 100

print(end_zeros)
print(zeros)
