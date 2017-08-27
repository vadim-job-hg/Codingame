# https://www.codingame.com/ide/puzzle/the-gift
import math
budget_left = []
budget_calculated=[]
oods_left = n = int(input())
cost_left = int(input())
for i in range(n):
    budget_left.append(int(input()))
    budget_calculated.append(0)
while oods_left>0:
    each_pay = math.floor(cost_left/oods_left)
    for i in range(n):
        if budget_left[i]==0:
            continue
        if(budget_left[i]<=each_pay):
            oods_left-=1
            budget_calculated[i] += budget_left[i]
            cost_left -= budget_left[i]
            budget_left[i] = 0
        else:
            budget_calculated[i] += each_pay
            cost_left -= each_pay
            budget_left[i] -= each_pay
        if cost_left==0:
            break
    if cost_left<oods_left:
        for i in range(n-1, 0, -1):
            if cost_left==0:
                break
            if budget_left[i]>0:
                budget_calculated[i] += 1
                cost_left -=1
    if cost_left==0:
        break
if oods_left==0 and cost_left>0:
    print("IMPOSSIBLE")
else:
    budget_calculated.sort()
    for b in budget_calculated:
        print(b)
