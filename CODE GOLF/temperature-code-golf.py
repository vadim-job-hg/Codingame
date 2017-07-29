e,v,W,B={},[],"WAIT",'BLOCK'
o,l,u,z,s,t,a,r=[int(i) for i in input().split()]
for i in range(r):
 v.append([int(j) for j in input().split()])
 e[v[i][0]]=v[i][1]
while 1:
 f,p,d=input().split()
 f,p=int(f),int(p)
 if f==z or f==-1:
  p=(W,B)[(p>s and d[:1]=='R')or(p<s and d[:1]=='L')]
 else:
  p=(W,B)[(p>e[f] and d[:1]=='R')or(p<e[f] and d[:1]=='L')]
 print(p)