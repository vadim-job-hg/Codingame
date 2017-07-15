# https://www.codingame.com/ide/puzzle/temperatures
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # the number of temperatures to analyse
temps = input()  # the n temperatures expressed as integers ranging from -273 to 5526
if n !=0:
    print(temps, file=sys.stderr)
    array = temps.split(' ')
    print(len(array), file=sys.stderr)
    min = int(array[0])
    for i in range(1, n):
        print(i, file=sys.stderr)
        if (abs(min)>abs(int(array[i]))  or (abs(min)==abs(int(array[i])) and int(array[i])>min)):
            min = int(array[i])
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
else:
    min = 0
print(str(min))



