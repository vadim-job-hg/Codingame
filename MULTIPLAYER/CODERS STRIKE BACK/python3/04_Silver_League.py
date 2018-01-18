import sys
import math

# Punto y coordenadas

class Punto:
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return "({},{})".format(self.x, self.y)
    
    def cuadrante(self):
        
        if self.x == 0:
            if self.y != 0:
                return 'El {} esta en el Eje Y'.format(self)
            else:
                return 'El {} esta en el Origen'.format(self)
        else:
            if self.y == 0:
                return 'El {} esta en el Eje X'.format(self)
    
        
        if self.x > 0:
            if self.y > 0:
                return 'El {} esta en el Cuadrante 1°'.format(self)
            else:
                return 'El {} esta en el Cuadrante 4°'.format(self)
        else:
            if self.y > 0:
                return 'El {} esta en el Cuadrante 2°'.format(self)
            else:
                return 'El {} esta en el Cuadrante 3°'.format(self)
        
    
    
    def vector(self, punto_b):
        #AB = (x2-x1, y2-y1)
        x = punto_b.x - self.x
        y = punto_b.y - self.y
        vector_ab = Punto(x, y)
        return vector_ab

    def distancia(self, punto_b):
        x = (punto_b.x - self.x) ** 2
        y = (punto_b.y - self.y) ** 2
        distancia_ab = math.sqrt(x + y)
        return distancia_ab

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

#initial variables
avaliable_boost = True
pod_diametre = 800
thrust = str(100)

# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    
    # Position of opponent and myself
    
    myself_point = Punto(x,y)
    opponnet_point = Punto(opponent_x, opponent_y)
    distant_myself_opponent = myself_point.distancia(opponnet_point)
    
    # Logical Pod
    #if thrust == 'SHIELD':
    #thrust = str(100)
    
    if next_checkpoint_angle > 80 or next_checkpoint_angle < -80:
        thrust = str(1)
        
        if next_checkpoint_angle > 120 or next_checkpoint_angle < -120:
            thrust = str(35)
    #elif next_checkpoint_angle > 45 or next_checkpoint_angle < -45:
     #   thrust = str(40)
    else:
        if  avaliable_boost and next_checkpoint_dist < 6000 and next_checkpoint_dist > 5000 and (next_checkpoint_angle  < 2 or next_checkpoint_angle  > -2):
            thrust = 'BOOST'
            avaliable_boost = False
        else:
            if next_checkpoint_dist < 2500 and next_checkpoint_dist > 1500:
                thrust = str(50)
            elif next_checkpoint_dist < 1000:
                thrust = str(90)
                #thrust = 'SHIELD'
            else:
                thrust = str(100)
                
    if distant_myself_opponent <= pod_diametre * 1.1:
        thrust = 'SHIELD'
  
    
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + thrust)
    #print('3618 3412 ' + thrust)
