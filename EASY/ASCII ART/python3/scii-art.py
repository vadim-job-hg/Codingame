# https://www.codingame.com/ide/puzzle/ascii-art
string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
l = int(input())
h = int(input())
t = input()
row = []
for i in range(h):
    row.append(input())
for i in range(h):
    word = ""
    for let in t:
        try:
            index = string.index(let.upper())
            word = word + row[i][(index * l):((index + 1) * l)]
        except ValueError:
            index = string.index("?")
            word = word + row[i][(index * l):((index + 1) * l)]
    print(word)