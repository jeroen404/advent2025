#!/usr/bin/env python3

from math import prod

class MathProblem:
    def __init__(self):
        self.operand = None
        self.terms = []
    def add_term(self, term):
        self.terms.append(term)
    def set_operand(self, operand):
        self.operand = operand
    def solve(self):
        if self.operand == '+':
            return sum(self.terms)
        elif self.operand == '*':
            return prod(self.terms)
        else:   
            raise ValueError(f"Unknown operand: {self.operand}")
        

inputs = []
try:
    while True:
        inputs.append(input())
except EOFError:
    pass

# part 1

first_line = inputs[0]
terms = [int(x) for x in first_line.split()]
mathproblems = [MathProblem() for _ in terms]
for i, term in enumerate(terms):
    mathproblems[i].add_term(term)
for line in inputs[1:-1]:
    parts = line.split()
    for i, part in enumerate(parts):
        term = int(part)
        mathproblems[i].add_term(term)
operands = inputs[-1].split()
for i, ch in enumerate(operands):
    mathproblems[i].set_operand(ch)
results = [mp.solve() for mp in mathproblems]
print(sum(results))

# part 2
operator_positions = [i for i, chr in enumerate(inputs[-1]) if (chr == '*') or (chr == '+')]
# index is from right to left
mathproblems: list[MathProblem] = []
length = max(len(line) for line in inputs)
start_pos = length - 1
for problem_index, stop_pos in enumerate(reversed(operator_positions)):
    operator = inputs[-1][stop_pos]
    mathproblems.append(MathProblem())
    mathproblems[-1].set_operand(operator)
    for i in range(stop_pos, start_pos + 1):  # range stop is exclusive
        number_string = ""
        for line in inputs[:-1]:
            char = line[i]
            if char == ' ':
                continue
            number_string += char
        if number_string:
            term = int(number_string)
            mathproblems[problem_index].add_term(term)
    start_pos = stop_pos - 2
# operator is left algned so there are no terms left

results = [mp.solve() for mp in mathproblems]
print(sum(results))