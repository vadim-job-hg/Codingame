# adapted from https://github.com/texus/codingame/blob/master/Community%20Puzzles/The%20greatest%20number.cs
import sys
n = int(input())
chars = input().split()
chars.sort()
if chars[-1] == "0":
    print(0, end='')
    exit(0)

if chars[0] == "-":
    print('-', end='')
    if chars[1] == ".":
        print(chars[2], end='')
        print('.', end='')
        for i in range(3, len(chars)):
            print(chars[i], end='')
    else:
        index = 1
        while (chars[index] == "0"):
            index += 1;
        for i in range(index, len(chars)):
            print(chars[i], end='')
else:
    if (chars[0] == "."):
        print(chars[-1], end='')
        for i in range(len(chars) - 2, 1, -1):
            print(chars[i], end='')
        if (chars[1] != "0"):
            print('.', end='')
            print(chars[1], end='')
    else:
        index = 1
        while (chars[index] == "0"):
            index += 1
        for i in range(len(chars), 0, -1):
            print(chars[i - 1], end='')
