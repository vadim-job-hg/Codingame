#todo:
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
connections = {}
connections = {}


def calculate(n, nt):
    global connections
    temp = [-1]
    for i in connections.get(n, []):
        if i!= nt:
            temp.append(calculate(i, n))
    return max(temp) + 1

n = int(input())  # the number of adjacency relations
keys = {}
for i in range(n):
    # xi: the ID of a person which is adjacent to yi
    # yi: the ID of a person which is adjacent to xi
    xi, yi = [int(j) for j in input().split()]
    k = keys.get(xi, 0)
    keys[xi] = k+1
    k = keys.get(yi, 0)
    keys[yi] = k+1
    connections.setdefault(xi, []).append(yi)
    connections.setdefault(yi, []).append(xi)
temp = []
for i, v in keys.items():
    if v>1:
        temp.append(calculate(i, -1))
print(min(temp))
