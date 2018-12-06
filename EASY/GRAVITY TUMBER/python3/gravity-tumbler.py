import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height = [int(i) for i in input().split()]
count = int(input())
rasters = []
odd = count % 2 == 0
for i in range(height):
    rasters.append(input())

for j in range(count):
    for i in range(len(rasters)):
        rasters[i] = sorted(rasters[i], reverse=True)
    rasters = list(zip(*rasters))

for rast in rasters:
    print(''.join(rast))
