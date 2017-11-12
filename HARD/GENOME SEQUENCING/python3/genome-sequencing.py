# based on https://github.com/aethersg/codingame-puzzle/blob/master/Python/hard/Genome%20Sequencing.py
import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def nested(strings):
    res = strings.pop()
    while len(strings) > 0:
        new = strings.pop()
        for i in range(len(new) + 1):
            subLast = min(i + len(res), len(new))
            if new[i:subLast] == res[:subLast - i]:
                res = new[:subLast] + res[subLast - i:] + new[i + len(res):]
                break
    return res


def permutations(l):
    if len(l) == 0:
        return [[]]
    else:
        res = []
        for head in l:
            l2 = l[:]
            l2.remove(head)
            for tail in permutations(l2):
                res.append([head] + tail)
        return res


n = int(input())
strings = []
for i in range(n):
    subseq = input()
    strings.append(subseq)

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

print(min(len(nested(p)) for p in permutations(strings)))