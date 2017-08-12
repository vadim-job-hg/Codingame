import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
connections = {}
connections = {}


def calculate(n):
    global connections
    temp = [-1]
    for i in connections.get(n, []):
        temp.append(calculate(i))
    return max(temp) + 1


print("Debug messages...", file=sys.stderr)

n = int(input())  # the number of adjacency relations
for i in range(n):
    # xi: the ID of a person which is adjacent to yi
    # yi: the ID of a person which is adjacent to xi
    xi, yi = [int(j) for j in input().split()]
    connections.setdefault(xi, []).append(yi)
    connections.setdefault(yi, []).append(xi)
temp = []
for i in connections.keys():
    temp.append(calculate(i))
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)


# The minimal amount of steps required to completely propagate the advertisement
print(min(temp))
