import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def getBestBloker(si, gat):
    global relations
    global visited
    min_dist, p1, p2 = sys.maxsize, 0, 0
    for g in gat:
        # print(g, file=sys.stderr)
        if g in relations:
            for r in relations[g]:
                visited.clear()
                dist = distanceMin(r, si)
                print(dist, file=sys.stderr)
                if min_dist > dist:
                    min_dist, p1, p2 = dist, r, g
    return [p1, p2]


def distanceMin(num, si, cnt=1):
    global relations
    global visited
    being = visited.get(num, False)
    if being != False:
        if being > cnt:
            visited[num] = cnt
        else:
            return sys.maxsize
    else:
        visited[num] = cnt

    if num == si:
        return cnt
    min_dist = sys.maxsize
    relation_list = relations.get(num, [])
    for rel in relation_list:
        min = distanceMin(rel, si, cnt + 1)
        if min_dist >= min:
            min_dist = min
    return min_dist


def unsetter(c1, c2):
    global relations
    relations[c1].remove(c2)
    relations[c2].remove(c1)


# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
gat = []
relations = {}
visited = {}
n, l, e = [int(i) for i in input().split()]
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    relations.setdefault(n2, []).append(n1)
    relations.setdefault(n1, []).append(n2)

print(relations, file=sys.stderr)
for i in range(e):
    ei = int(input())  # the index of a gateway node
    gat.append(ei)

# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    c1, c2 = getBestBloker(si, gat)
    unsetter(c1, c2)
    print("{0} {1}".format(c1, c2))
    # Example: 3 4 are the indices of the nodes you wish to sever the link between