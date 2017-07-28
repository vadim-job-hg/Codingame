n,a=int(input()),[int(i)for i in input().split()]
m=(0,2**9)[n>0]
for i in a:
 m=(m,i)[abs(m)>abs(i)or(abs(m)==abs(i)and i>m)]
print(m)