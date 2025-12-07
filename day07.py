#!/usr/bin/env python3



tachyon_manifold = []
try:
    while True:
        tachyon_manifold.append(list(input()))
except EOFError:
    pass


start = tachyon_manifold[0].index('S')
tachyon_manifold[1][start] = '|'

splits = 0
timelines = [[0 for _ in range(len(tachyon_manifold[0]))] for _ in range(len(tachyon_manifold))] # init to all zeros
timelines[1][start] = 1

for i, line in enumerate(tachyon_manifold[2:], start=2):
    for j, ch in enumerate(line):
        if ch == '.' and tachyon_manifold[i-1][j] == '|':
            tachyon_manifold[i][j] = '|'
            timelines[i][j] = timelines[i-1][j]
        if ch == '^' and tachyon_manifold[i-1][j] == '|':
            splits += 1
            if j > 0:
                above_timeline = 0
                if tachyon_manifold[i][j-1] != '|':
                    tachyon_manifold[i][j-1] = '|'
                    above_timeline = timelines[i-1][j-1]
                timelines[i][j-1] += timelines[i-1][j] + above_timeline
            if j < len(line) - 1:
                above_timeline = 0
                if tachyon_manifold[i][j+1] != '|':
                    tachyon_manifold[i][j+1] = '|'
                    above_timeline = timelines[i-1][j+1]
                timelines[i][j+1] += timelines[i-1][j] + above_timeline

# part 1
print(splits)
# part 2
final_timelines = sum(timelines[-1][j] for j, ch in enumerate(tachyon_manifold[-1]) if ch == '|')
print(final_timelines)

# real    0m0.018s
# don't understand all the tree search and cache memes on reddit