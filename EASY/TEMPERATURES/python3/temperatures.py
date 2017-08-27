# https://www.codingame.com/ide/puzzle/temperatures
n = int(input())  # the number of temperatures to analyse
temps = input()  # the n temperatures expressed as integers ranging from -273 to 5526
if n !=0:
    array = temps.split(' ')
    min = int(array[0])
    for i in range(1, n):
        if (abs(min)>abs(int(array[i]))  or (abs(min)==abs(int(array[i])) and int(array[i])>min)):
            min = int(array[i])
else:
    min = 0
print(str(min))



