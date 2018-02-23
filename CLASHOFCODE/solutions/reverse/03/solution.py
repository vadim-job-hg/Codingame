import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

s = input()

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(sum([int(c.islower()) for c in s]))