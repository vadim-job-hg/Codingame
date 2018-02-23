import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

s = input()

numbers = sum(c.isdigit() for c in s)
words   = sum(c.isalpha() for c in s)
spaces  = sum(c.isspace() for c in s)
print(int(round(words/numbers, 0)))