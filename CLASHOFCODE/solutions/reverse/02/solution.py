import sys
import math

def quer(i):
    sum=0
    for c in str(i):
        sum+=int(c)
    return sum

n = int(input())

print(n+quer(n))