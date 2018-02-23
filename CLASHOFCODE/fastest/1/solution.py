import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
for i in range(n):
    line = input()
    for j in range(10):
        if str(j) not in line:
            print(j)