elv,elva={},[]
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in input().split()]
for i in range(nb_elevators):
 elva.append([int(j) for j in input().split()])
 elv[elva[i][0]]=elva[i][1]
while 1:
 clone_floor, clone_pos, direction = input().split()
 clone_floor = int(clone_floor)
 clone_pos = int(clone_pos)
 if clone_floor==exit_floor or clone_floor==-1 :
  #p = ()[]
  if clone_pos>exit_pos and direction=='RIGHT':
   p ='BLOCK'
  elif clone_pos<exit_pos and direction=='LEFT':
   p = 'BLOCK'
  else:
   p = "WAIT"
 else:
  if nb_floors>0:
   posi=elv[clone_floor]
   if clone_pos>posi and direction=='RIGHT':
    p = 'BLOCK'
   elif clone_pos<posi and direction=='LEFT':
    p = 'BLOCK'
   else:
    p ="WAIT"
print(p)