# https://www.codingame.com/ide/puzzle/7-segment-display
# https://github.com/aethersg/codingame-puzzle/blob/master/Python/community%20puzzle/7-segment%20display.py
import sys
import math
import copy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
c = raw_input()
s = int(raw_input())

integer_to_display = int(n)
number_string = str(copy.copy(integer_to_display))
character_to_display = c
segment_size = int(s)
width = segment_size + 2
height = (segment_size * 2) + 3


# print >> sys.stderr, "interger %s" % integer_to_display
# print >> sys.stderr, "charater_to_display %s" % charater_to_display
# print >> sys.stderr, "width %s" % width
# print >> sys.stderr, "height %s" % height

def create_character(w, h):
    array = [[" " for x in range(w)] for y in range(h)]
    return array


def fill_horizontal(char, array, x, y):
    start = x
    end = width - 1
    for i in range(start, end):
        array[y][i] = char


def fill_vertical(char, array, x, y):
    start = y
    end = y + segment_size
    for i in range(start, end):
        array[i][x] = char


def seg_1(char, ia):
    fill_horizontal(char, ia, 1, 0)


def seg_2(char, ia):
    fill_vertical(char, ia, 0, 1)


def seg_3(char, ia, w):
    fill_vertical(char, ia, (w - 1), 1)


def seg_4(char, ia, h):
    fill_horizontal(char, ia, 1, (h / 2))


def seg_5(char, ia, h):
    fill_vertical(char, ia, 0, ((h / 2) + 1))


def seg_6(char, ia, w, h):
    fill_vertical(char, ia, (w - 1), ((h / 2) + 1))


def seg_7(char, ia, h):
    fill_horizontal(char, ia, 1, (h - 1))


def create_array(width, height):
    integer_array = create_character(width, height)

    if inte == "0":
        seg_1(character_to_display, integer_array)
        seg_2(character_to_display, integer_array)
        seg_3(character_to_display, integer_array, width)
        seg_5(character_to_display, integer_array, height)
        seg_6(character_to_display, integer_array, width, height)
        seg_7(character_to_display, integer_array, height)
    elif inte == "1":
        seg_3(character_to_display, integer_array, width)
        seg_6(character_to_display, integer_array, width, height)
    elif inte == "2":
        seg_1(character_to_display, integer_array)
        seg_3(character_to_display, integer_array, width)
        seg_4(character_to_display, integer_array, height)
        seg_5(character_to_display, integer_array, height)
        seg_7(character_to_display, integer_array, height)
    elif inte == "3":
        seg_1(character_to_display, integer_array)
        seg_3(character_to_display, integer_array, width)
        seg_4(character_to_display, integer_array, height)
        seg_6(character_to_display, integer_array, width, height)
        seg_7(character_to_display, integer_array, height)
    elif inte == "4":
        seg_2(character_to_display, integer_array)
        seg_3(character_to_display, integer_array, width)
        seg_4(character_to_display, integer_array, height)
        seg_6(character_to_display, integer_array, width, height)
    elif inte == "5":
        seg_1(character_to_display, integer_array)
        seg_2(character_to_display, integer_array)
        seg_4(character_to_display, integer_array, height)
        seg_6(character_to_display, integer_array, width, height)
        seg_7(character_to_display, integer_array, height)
    elif inte == "6":
        seg_1(character_to_display, integer_array)
        seg_2(character_to_display, integer_array)
        seg_4(character_to_display, integer_array, height)
        seg_5(character_to_display, integer_array, height)
        seg_6(character_to_display, integer_array, width, height)
        seg_7(character_to_display, integer_array, height)
    elif inte == "7":
        seg_1(character_to_display, integer_array)
        seg_3(character_to_display, integer_array, width)
        seg_6(character_to_display, integer_array, width, height)
    elif inte == "8":
        seg_1(character_to_display, integer_array)
        seg_2(character_to_display, integer_array)
        seg_3(character_to_display, integer_array, width)
        seg_4(character_to_display, integer_array, height)
        seg_5(character_to_display, integer_array, height)
        seg_6(character_to_display, integer_array, width, height)
        seg_7(character_to_display, integer_array, height)
    elif inte == "9":
        seg_1(character_to_display, integer_array)
        seg_2(character_to_display, integer_array)
        seg_3(character_to_display, integer_array, width)
        seg_4(character_to_display, integer_array, height)
        seg_6(character_to_display, integer_array, width, height)
        seg_7(character_to_display, integer_array, height)

    return integer_array

main_array = []
for inte in number_string:
    array = create_array(width, height)
    if not main_array:
        main_array = array
    else:
        for no in range(len(main_array)):
            main_array[no].append(" ")
            for n in array[no]:
                main_array[no].append(n)


for a in main_array:
    line = ""
    for c in a:
        line += c
    answer = line.rstrip()
    print answer