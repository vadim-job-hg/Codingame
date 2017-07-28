n,array=int(input()),input().split()
if n>0:
 min=int(array[0])
 for i in range(1,n):
  if(abs(min)>abs(int(array[i]))or(abs(min)==abs(int(array[i]))and int(array[i])>min)):
   min=int(array[i])
else:
 min=0
print(min)