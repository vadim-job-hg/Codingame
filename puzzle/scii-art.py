# https://www.codingame.com/ide/puzzle/ascii-art
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
l = int(input())
h = int(input())
t = input()
row = []
for i in range(h):
    row.append(input())
    # print(row[(index*l):((index+1)*l)])
for i in range(h):
    word = ""
    for let in t:
        try:
            index = string.index(let.upper())
            print(i, file=sys.stderr)
            word = word + row[i][(index * l):((index + 1) * l)]
        except ValueError:
            index = string.index("?")
            word = word + row[i][(index * l):((index + 1) * l)]
    print(word)

# print(index, file=sys.stderr)
# print(row[index:l])
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
# print(l, file=sys.stderr)
# print(row, file=sys.stderr)
# print("#")
