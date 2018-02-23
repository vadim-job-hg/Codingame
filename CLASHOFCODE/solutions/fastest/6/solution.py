import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
s = 0
for i in input().split():
    s+= int(i)**2

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(s)