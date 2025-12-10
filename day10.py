#!/usr/bin/env python3

#part 1
import heapq

# part 2
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

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
    def press_until_on(self) -> int:
        nblights = len(self.indicator_lights_pattern)
        initial_pattern = tuple([False] * nblights) # patterns are tuples of lists of bools to make them hashable
        visited_patterns = set()
        pq = []
        heapq.heappush(pq, (0, initial_pattern))
        while pq:
            presses, pattern = heapq.heappop(pq)
            if pattern in visited_patterns:
                continue # already visited and number of presses is equal or higher this time
            visited_patterns.add(pattern)
            if machine.machine_on(list(pattern)):
                return presses
            for button_index in range(len(machine.buttons)):
                new_pattern_list = machine.press_button(button_index, list(pattern))
                new_pattern = tuple(new_pattern_list)
                heapq.heappush(pq, (presses + 1, new_pattern))
        return -1  # impossible
    #
    # part 2
    # just pressed tab to let copilot fill in the rest and then corrected it
    def press_until_powered_on(self) -> int:
        nbjoltages = len(self.joltage_requirements)
        nbbuttons = len(self.buttons)
        c = np.ones(nbbuttons)
        A = np.zeros((nbjoltages, nbbuttons))  # all zero matrix
        for button_index, button in enumerate(self.buttons):
            for light_index in button:
                A[light_index, button_index] = 1  # A[i,j] = 1 if button j addes 1 to joltage i
        b = np.array(self.joltage_requirements)
        bounds = Bounds(0, np.inf)
        linear_constraint = LinearConstraint(A, b, b)
        res = milp(c=c, constraints=[linear_constraint], bounds=bounds, integrality=np.ones(nbbuttons))
        if res.success:
            return int(res.fun)
        else:
            return -1  # impossible
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

machines = []
try:
    while True:
        line = input()
        machines.append(Machine.from_string(line))
except EOFError:
    pass

total_presses = 0
for machine in machines:
    presses = machine.press_until_on()
    total_presses += presses
print(f"Total button presses for all machines: {total_presses}")

total_presses_powered = 0
for machine in machines:
    presses = machine.press_until_powered_on()
    total_presses_powered += presses
print(f"Total button presses to power on all machines: {total_presses_powered}")


