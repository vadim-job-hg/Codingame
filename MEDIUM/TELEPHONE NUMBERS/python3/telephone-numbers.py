# https://www.codingame.com/ide/puzzle/telephone-numbers
import sys
import math
data = {}
n = int(input())
cnt = 0
for i in range(n):
    telephone = input()
    temp = data
    for t in telephone:
        val = temp.get(t, None)
        if val == None:
            cnt+=1
        temp = temp.setdefault(t, {})
# The number of elements (referencing a number) stored in the structure.
print(cnt)
