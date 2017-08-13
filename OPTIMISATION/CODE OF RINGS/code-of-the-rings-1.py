import sys
import math

LETTERS_PLUS = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS_MINUS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "[::-1]


def closest_plus(char):
    return LETTERS_PLUS.find(char)


def closest_minus(char):
    return LETTERS_MINUS.find(char)


magic_phrase = input()
print(magic_phrase, file=sys.stderr)
path = sight = ""
for char in magic_phrase:
    plus = closest_plus(char)
    minus = closest_minus(char)
    sight, count = (["-", minus], ["+", plus])[plus < minus]
    print(sight, count, file=sys.stderr)
    path = path + (sight * count) + ".>"
print(path)