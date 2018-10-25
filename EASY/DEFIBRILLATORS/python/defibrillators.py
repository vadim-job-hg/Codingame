# https://www.codingame.com/ide/puzzle/defibrillators
import sys
import math
def get_distance(lat_a, lat_b, long_a, long_b):
    x = (long_b - long_a) * math.cos((lat_b + lat_a) / 2)
    y = lat_b - lat_a
    return math.sqrt(x * x + y * y) * 6371


lon = raw_input()
lat = raw_input()
n = int(raw_input())
current = {}
closest = 3.402823e+38
for i in range(n):
    defib = {}
    defib['id'], defib['name'], defib['address'], defib['phone'], defib['long'], defib['lat'] = [j for j in
                                                                                                 raw_input().split(';')]
    distance = get_distance(float(lat.replace(',', '.')), float(defib['lat'].replace(',', '.')),
                            float(lon.replace(',', '.')), float(defib['long'].replace(',', '.')))
    if distance < closest:
        current = defib
        closest = distance
print(current['name'])
