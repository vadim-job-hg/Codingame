import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

s = input()
a = len(s)%2
print("".join(s[0::2]+s[a*-1-1::-2]))