# https://www.codingame.com/ide/puzzle/horse-racing-duals
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
pi = []
n = int(input())
for i in range(n):
    pi.append(int(input()))
pi.sort()
#print(pi, file=sys.stderr)

min = 10000000
for i in range(n-1):    
    if min>abs(pi[i]-pi[i+1]):
        min = abs(pi[i]-pi[i+1])
        if min==0:
            break
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(min)
