# https://www.codingame.com/training/medium/stock-exchange-losses
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
diff = 0
graf = []
n = int(input())
for i in input().split():
    graf.append(int(i))
for i in range(n - 1):
    for j in range(i + 1, n):
        if graf[i] < graf[j]:
            i = j
            break
        elif diff < graf[i] - graf[j]:
            diff = graf[i] - graf[j]

if diff != 0:
    print("-" + str(diff))
else:
    print("0")
