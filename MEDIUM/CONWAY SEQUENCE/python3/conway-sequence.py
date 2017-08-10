#https://www.codingame.com/ide/puzzle/conway-sequence
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

r = int(input())
l = int(input())
#print(r, file=sys.stderr)
#print(l, file=sys.stderr)
str_s = []
array = [r]
for i in range(1, l):
    new_array = []
    num, last = 0, -1
    for v in array:
        if v != last:
            if num != 0:
                new_array.append(num)
                new_array.append(last)
            num = 1
        else:
            num +=1
        last = v
    new_array.append(num)
    new_array.append(last)
    #print(new_array, file=sys.stderr)
    array = new_array
print( ' '.join(str(v) for v in array))