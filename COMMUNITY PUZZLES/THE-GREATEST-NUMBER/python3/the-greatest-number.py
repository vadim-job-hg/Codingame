# adapted from https://github.com/texus/codingame/blob/master/Community%20Puzzles/The%20greatest%20number.cs
import sys
import math

n = int(input())
maimum = True
dot = False
numbers = []
string = ""
for i in input().split():
    if i == '.':
        dot = True
    elif i == '-':
        maimum = False
    else:
        numbers.append(int(i))

if maimum:
    numbers.sort(reverse=True)
else:
    numbers.sort()
    string += "-"
print(numbers, file=sys.stderr)
for i in range(len(numbers)):
    if ((i == len(numbers) - 1 and maimum) or (i == 1 and not (maimum))) and dot:
        string += "."
    string += str(numbers[i])
print(string)
