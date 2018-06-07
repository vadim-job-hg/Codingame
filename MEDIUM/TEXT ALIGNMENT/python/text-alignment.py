# https://www.codingame.com/ide/puzzle/text-alignment
# got from https://github.com/aethersg/codingame-puzzle/blob/master/Python/community%20puzzle/text%20align.py
import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def words_len(array):
    return sum([len(x) for x in array])


def justify(sentence, width):
    words = sentence.split(" ")
    extra_space = width - words_len(words)
    while extra_space > 0 and len(words) > 1:
        for i in range(len(words) - 1):
            words[i] += " "
            extra_space -= 1
            if extra_space < 1:
                break;
    return ''.join(words)


alignment = raw_input()
n = int(raw_input())

map_line = []
max_size = 0
for i in xrange(n):
    text = raw_input()
    max_size = max(len(text), max_size)
    map_line.append(text)

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."
for t in map_line:
    if alignment == "LEFT":
        print t.ljust(0)
    if alignment == "RIGHT":
        print t.rjust(max_size)
    if alignment == "CENTER":
        print t.center(max_size).rstrip()
    if alignment == "JUSTIFY":
        print justify(t, max_size)