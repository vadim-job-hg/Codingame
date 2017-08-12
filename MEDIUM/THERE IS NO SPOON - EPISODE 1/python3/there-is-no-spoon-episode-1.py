# https://www.codingame.com/ide/puzzle/there-is-no-spoon-episode-1
import sys
import math

# Don't let the machines win. You are humanity's last hope...

width = int(input())  # the number of cells on the X axis
height = int(input())  # the number of cells on the Y axis
lines = []
for i in range(height):
    line = input()  # width characters, each either 0 or .
    lines.append(list(line))
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
for y in range(height):
    for x in range(width):
       if lines[y][x]==".":
           continue
       rx = ry = bx = by = -1
       try:
           for tx in range(x+1,width):
               if(lines[y][tx]=='0'):
                   rx = tx
                   ry = y
                   break
       except Exception:
           pass
       try:
           for ty in range(y+1, height):
               if(lines[ty][x]=='0'):
                   bx = x
                   by =ty
                   break
       except Exception:
           pass
       print("{0} {1} {2} {3} {4} {5}".format(x, y, rx, ry, bx, by))

