# https://www.codingame.com/ide/puzzle/paper-folding-curve
# from https://github.com/frostming/Codingame/blob/master/Puzzle-of-the-Week/paper_folding_curve.py
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

order = int(input())
s, e = [int(i) for i in input().split()]
print(s, e, file=sys.stderr)
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

original = '01101100'


def get_bit(n):
    if not n & (n - 1):
        return '1'
    while n & 1 == 0:
        n >>= 1
    if n & 3 == 3:
        return '0'
    else:
        return '1'


answer = ''.join(get_bit(i) for i in range(s + 1, e + 2))
print(answer)