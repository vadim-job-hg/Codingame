import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways

def getBestBloker(si, gat):
    global relations
    for g in gat:
        if g in relations[si]:
            return [si, g]
    for g in gat:
        if len(relations[g]) > 0:
            return [g, relations[g][0]]
    return [0, 0]


def unsetter(c1, c2):
    global relations
    relations[c1].remove(c2)
    relations[c2].remove(c1)


n, l, e = [int(i) for i in input().split()]
gat = []
relations = {}
print("LINKS: ", file=sys.stderr)
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    print(n1, n2, file=sys.stderr)
    relations.setdefault(n1, []).append(n2)
    relations.setdefault(n2, []).append(n1)
print(relations, file=sys.stderr)
print("Exit gateways: ", file=sys.stderr)
for i in range(e):
    ei = int(input())  # the index of a gateway node
    print(ei, file=sys.stderr)
    gat.append(ei)
print("GAME: ", file=sys.stderr)
# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    print(si, file=sys.stderr)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    c1, c2 = getBestBloker(si, gat)
    unsetter(c1, c2)
    # Example: 0 1 are the indices of the nodes you wish to sever the link between
    print("{0} {1}".format(c1, c2))
