# https://www.codingame.com/ide/puzzle/bust-speeding-vehicles
import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def check_speed(cur_car, car, km, timestamp):
    kilometers = km - cur_car['km']
    # print("kilometers: " + str(kilometers), file=sys.stderr)
    hours = (timestamp - cur_car['timestamp']) / 3600
    # print("hours: " + str(hours), file=sys.stderr)
    speed = kilometers / hours
    # print("speed: " + str(speed), file=sys.stderr)
    return speed


L_MAX = 100
L_MIN = 10
N_MAX = 100
C_MAX = 1000
l = int(input())
# print(l, file=sys.stderr)
n = int(input())
cars = {}
ok = True
for i in range(n):
    car, km, timestamp = input().split()
    # print(car, km, timestamp, file=sys.stderr)
    cur_car = cars.get(car, None)
    if cur_car is not None:
        speed = check_speed(cur_car, car, int(km), int(timestamp))
        if speed > l:
            print("{0} {1}".format(car, km))
            ok = False
    cars[car] = {'car': car, 'km': int(km), 'timestamp': int(timestamp)}
if ok:
    print("OK")

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
