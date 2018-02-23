import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
e=[]
for i in range(n):
    s, d = [int(j) for j in input().split()]
    e.append(round(d/(s/60)))

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(min(e))