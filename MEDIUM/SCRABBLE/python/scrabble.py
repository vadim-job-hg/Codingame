# https://www.codingame.com/ide/puzzle/scrabble
values = {
    'e':1, 'a':1, 'i':1, 'o':1, 'n':1, 'r':1, 't':1, 'l':1, 's':1, 'u':1,
    'd':2, 'g':2,
    'b':3, 'c':3, 'm':3, 'p':3,
    'f':4, 'h':4, 'v':4, 'w':4, 'y':4,
    'k':5,
    'j':6, 'x':6,
    'q':7, 'z':7
    }
words = []
n = int(raw_input())
for i in range(n):
    w = raw_input()
    words.append(w)
letters = raw_input()
max, winword = 0, ''
for word in words:
    temp = 0
    temp_letters = list(letters)
    for letter in word:
        if (letter in temp_letters):
            temp+=values[letter]
            try:
                temp_letters.remove(letter)
            except ValueError:
                temp = -1
                break
        else:
            temp = -1
            break
    if temp>max:
        max = temp
        winword = word
print(winword)