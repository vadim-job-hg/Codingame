# https://www.codingame.com/ide/puzzle/telephone-numbers
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
data = {}
n = int(input())
cnt = 0
for i in range(n):
    telephone = input()
    temp = data
    for t in telephone:
        val = temp.get(t, None)
        if val == None:
            cnt+=1
        temp = temp.setdefault(t, {})
print(data, file=sys.stderr)
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)


# The number of elements (referencing a number) stored in the structure.
print(cnt)
