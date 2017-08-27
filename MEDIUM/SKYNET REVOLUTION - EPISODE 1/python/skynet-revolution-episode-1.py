#https://www.codingame.com/ide/puzzle/skynet-revolution-episode-1
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
for i in range(l):
    n1, n2 = [int(j) for j in input().split()]
    relations.setdefault(n1, []).append(n2)
    relations.setdefault(n2, []).append(n1)
for i in range(e):
    ei = int(input())
    gat.append(ei)
# game loop
while True:
    si = int(input())
    c1, c2 = getBestBloker(si, gat)
    unsetter(c1, c2)
    print("{0} {1}".format(c1, c2))
