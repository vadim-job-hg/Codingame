# https://www.codingame.com/ide/puzzle/shadows-of-the-knight-episode-2
# https://www.codingame.com/ide/puzzle/shadows-of-the-knight-episode-1
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in input().split()]
matrix = [[0 for _ in range(w)] for i in range(h)]


def calcLength(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def fillMatrixAndFindCoors(x0, y0):
    global matrix
    for y in len(matrix):
        for x in len(matrix):
            matrix[y][x] = calcLength(x, y, x0, y0)


while True:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    print(bomb_dir, file=sys.stderr)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    if bomb_dir.find("WARMER") > -1:
        maxy = y0 - 1
    elif bomb_dir.find("COLDER") > -1:
        miny = y0 + 1
    elif bomb_dir.find("SAME") > -1:
        maxx = x0 - 1
    elif bomb_dir.find("R") > -1:
        minx = x0 + 1
    print(minx, miny, maxx, maxy, file=sys.stderr)
    x0 = minx + math.ceil((maxx - minx) / 2)
    y0 = miny + math.ceil((maxy - miny) / 2)
    # the location of the next window Batman should jump to.
    print("{0} {1}".format(x0, y0))
