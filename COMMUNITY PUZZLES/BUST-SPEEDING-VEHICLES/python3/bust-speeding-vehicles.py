# https://www.codingame.com/ide/puzzle/bust-speeding-vehicles
def check_speed(cur_car, car, km, timestamp):
    kilometers = km - cur_car['km']
    hours = (timestamp - cur_car['timestamp']) / 3600
    speed = kilometers / hours
    return speed
L_MAX = 100
L_MIN = 10
N_MAX = 100
C_MAX = 1000
l = int(input())
n = int(input())
cars = {}
ok = True
for i in range(n):
    car, km, timestamp = input().split()
    cur_car = cars.get(car, None)
    if cur_car is not None:
        speed = check_speed(cur_car, car, int(km), int(timestamp))
        if speed > l:
            print("{0} {1}".format(car, km))
            ok = False
    cars[car] = {'car': car, 'km': int(km), 'timestamp': int(timestamp)}
if ok:
    print("OK")