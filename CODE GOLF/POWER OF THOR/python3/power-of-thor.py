x,y,z,w=[int(i)for i in input().split()]
while 1:m,w=(((["",w],["N",w-1])[w>y]),["S",w+1])[w<y]; m,z=((([m,z],[m+"W",z-1])[z>x]),[m+"E",z+1])[z<x];print(m);