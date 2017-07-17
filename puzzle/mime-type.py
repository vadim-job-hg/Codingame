# https://www.codingame.com/ide/puzzle/mime-type
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
print(dictionary, file=sys.stderr)
for i in range(q):
    fname = input()  # One file name per line.    
    print(fname, file=sys.stderr)
    farr = fname.split('.')
    #print(farr[-1], file=sys.stderr)
    if len(farr)>1:
        try:
            print(dictionary[farr[-1]])
        except KeyError:
            print("UNKNOWN")
        except IndexError:
            print("UNKNOWN")
    else:
        print("UNKNOWN")
    #print(farr[1], file=sys.stderr)
    #print(dictionary.keys(), file=sys.stderr)
    #print(dictionary[farr[1]], file=sys.stderr)
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)


# For each of the Q filenames, display on a line the corresponding MIME type. If there is no corresponding type, then display UNKNOWN.

