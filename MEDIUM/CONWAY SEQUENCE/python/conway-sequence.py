#https://www.codingame.com/ide/puzzle/conway-sequence
import sys
import math
r = int(raw_input())
l = int(raw_input())
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
    array = new_array
print( ' '.join(str(v) for v in array))