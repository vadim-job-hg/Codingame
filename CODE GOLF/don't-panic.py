elevator_coors =[]
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [
   int(i) for i in input().split()]
for i in range(nb_elevators):
 elevator_floor, elevator_pos = [int(j) for j in input().split()]
 elevator_coors(elevator_floor, []).append(elevator_pos)
while True:
 clone_floor, clone_pos, direction, wait = input().split(),0
 clone_floor = int(clone_floor)
 clone_pos = int(clone_pos)
 if wait>0:
     wait-=wait
     print("WAIT")