# based on https://github.com/aethersg/codingame-puzzle/blob/master/Python/hard/Super%20Computer.py
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
array = []
last_date = 0
for i in range(n):
    j, d = [int(j) for j in input().split()]
    array.append((j, j + d))
    last_date = max(last_date, array[i][1])

array.sort(key=lambda a: a[1])

timeline = [0] * last_date
answer = 0
for a in array:
    if not 1 in timeline[a[0]:a[1]]:
        answer += 1
        timeline[a[0]:a[1]] = [1] * (a[1] - a[0])

print(answer)