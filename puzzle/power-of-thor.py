lx,ly,initial_tx,initial_ty=[int(i)for i in input().split()]
while int(input()):
 m=""
 if initial_ty<ly:
  m="S"
  initial_ty=initial_ty+1
 elif initial_ty>ly:
  m="N"
  initial_ty=initial_ty-1
 if initial_tx<lx:
  m=m+"E"
  initial_tx=initial_tx+1
 elif initial_tx>lx:
  m=m+"W"
  initial_tx=initial_tx-1
print(m)