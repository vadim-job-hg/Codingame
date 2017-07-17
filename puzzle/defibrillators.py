# https://www.codingame.com/ide/puzzle/defibrillators
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def get_distance(lat_a, lat_b, long_a, long_b):
    print(lat_a, lat_b, long_a, long_b, file=sys.stderr)
    x = (long_b - long_a)*math.cos((lat_b + lat_a)/2)
    y = lat_b - lat_a
    return math.sqrt(x*x +y*y)*6371
    
lon = input()
lat = input()
n = int(input())
current = {}
closest = 3.402823e+38
for i in range(n):
    defib = {}
    defib['id'], defib['name'], defib['address'], defib['phone'], defib['long'], defib['lat']  = [j for j in input().split(';')]
    distance = get_distance(float(lat.replace(',', '.')), float(defib['lat'].replace(',', '.')), float(lon.replace(',', '.')), float(defib['long'].replace(',', '.')))
    print(defib, file=sys.stderr)
    print(distance, file=sys.stderr)
    if distance<closest:
        current = defib
        closest = distance
print(current, file=sys.stderr)
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(current['name'])
