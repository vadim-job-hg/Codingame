x,y,z,w=[int(i)for i in input().split()]
while 1:
 #m = (5, 100)[t == 0]
 m,w=["S",w+1] if w<y else ["N",w-1] if w>y else ["",w]
 m,z=[m+"E",z+1] if z<x else [m+"W",z-1] if z>x else [m,z] 
 print m