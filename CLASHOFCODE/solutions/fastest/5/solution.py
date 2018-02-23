import sys
import math
n = int(input())
s = input()
r = 0
for i in s:
    t = int(i)
    if t==0:
        r=0
    else:
        r+=t
print(r)