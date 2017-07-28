# FROM HERE https://github.com/kpbochenek/algorithms/blob/master/codingame/medium/network-cabling.py
N = int(input())
housesX = []
housesY = []
for i in range(N):
    X, Y = [int(i) for i in input().split()]
    housesX.append(X)
    housesY.append(Y)

housesY.sort()
meanlow = housesY[len(housesY)//2]
meanhigh = housesY[len(housesY)//2+1] if len(housesY) > 1 else housesY[0]

# To debug: print("Debug messages...", file=sys.stderr)
lowest = min(housesX)
highest = max(housesX)
result1 = sum(map(lambda y: abs(meanlow - y), housesY))
result2 = sum(map(lambda y: abs(meanhigh - y), housesY))

print(min(result1, result2) + highest - lowest)