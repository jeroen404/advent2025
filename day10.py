#!/usr/bin/env python3

import heapq

class Machine:
    def __init__(self, indicator_lights_pattern: list[bool], buttons: list[frozenset[int]], joltage_requirements: list[int]):
        self.indicator_lights_pattern: list[bool] = indicator_lights_pattern
        self.buttons: list[frozenset[int]] = buttons
        self.joltage_requirements: list[int] = joltage_requirements
    def __repr__(self) -> str:
        return f"Machine(lights={self.indicator_lights_pattern}, buttons={self.buttons}, joltage={self.joltage_requirements})"
    def machine_on(self, indicator_light_pattern: list[bool]) -> bool:
        return self.indicator_lights_pattern == indicator_light_pattern 
    def press_button(self, button_index: int, start_pattern: list[bool]) -> list[bool]:
        new_pattern = start_pattern.copy()
        button = self.buttons[button_index]
        for light_index in button:
            new_pattern[light_index] = not new_pattern[light_index]
        return new_pattern
    @staticmethod
    def from_string(s: str) -> 'Machine':
        parts = s.split()
        lights_part = parts[0].strip()
        indicator_lights = [c == '#' for c in lights_part.strip('[]')]
        buttons = []
        for button_part in parts[1:-1]:
            button_set = frozenset(int(x) for x in button_part.strip('()').split(',') if x)
            buttons.append(button_set)
        joltage_requirements = [int(x) for x in parts[-1].strip('{}').split(',') if x]
        return Machine(indicator_lights, buttons, joltage_requirements)

def pattern_to_string(pattern: list[bool]) -> str:
    return ''.join('#' if light else '.' for light in pattern)

def press_until_on(machine: Machine) -> int:
    nblights = len(machine.indicator_lights_pattern)
    initial_pattern = tuple([False] * nblights)
    visited_patterns = set()
    pq = []
    heapq.heappush(pq, (0, initial_pattern))
    while pq:
        presses, pattern = heapq.heappop(pq)
        
        if pattern in visited_patterns:
            continue
        visited_patterns.add(pattern)
        if machine.machine_on(list(pattern)):
            return presses
        for button_index in range(len(machine.buttons)):
            new_pattern_list = machine.press_button(button_index, list(pattern))
            new_pattern = tuple(new_pattern_list)
            heapq.heappush(pq, (presses + 1, new_pattern))
    return -1  # impossible


machines = []
try:
    while True:
        line = input()
        machines.append(Machine.from_string(line))
except EOFError:
    pass

total_presses = 0
for machine in machines:
    presses = press_until_on(machine)
    #print(f"Minimum button presses to turn on machine {machine}: {presses}")
    total_presses += presses
print(f"Total button presses for all machines: {total_presses}")