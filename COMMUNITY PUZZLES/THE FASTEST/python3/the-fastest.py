import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
timew = '23:59:59'
minimum = 23*60*60 + 59*60 + 59
n = int(input())
for i in range(n):
    t = input()
    print(t, file=sys.stderr)
    temp = t.split(':')
    time = int(temp[0])*60*60 + int(temp[1])*60 + int(temp[2])
    if time<minimum:
        minimum = time
        timew = t


# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(timew)
