import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
dictionary = {}
n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.
for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = input().split()
    dictionary[ext] = mt    
for i in range(q):
    fname = input()  # One file name per line.
    farr = fname.split('.')
    if farr[1] and farr[1] in dictionary:
        print(dictionary[farr[1]])
    else:
        print("UNKNOWN")

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)


# For each of the Q filenames, display on a line the corresponding MIME type. If there is no corresponding type, then display UNKNOWN.

