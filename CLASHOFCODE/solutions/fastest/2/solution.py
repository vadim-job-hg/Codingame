import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

string = input()
stri = ""
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
t = len(string)
s = 1
for i in range(len(string)):
    stri += (string[(i + s) % t])
    s += i + 2

print(stri)