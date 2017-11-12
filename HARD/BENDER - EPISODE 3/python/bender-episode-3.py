import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
# print n
points = []
for i in xrange(n):
    num, t = [int(j) for j in raw_input().split()]
    points.append([num, t])


# print points

def trapezoidal_rule(points, a, b, n):
    h = (float)(b - a) / n
    # print "H", h,
    I = 0.0
    for i in range(n - 1):
        I += (points[i + 1][0] - points[i][0]) * (points[i][1] + points[i + 1][1])
    I = (float)(h * I) / 2
    return I


# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."
a = points[0][0]
b1 = points[n - 1][0]
b2 = points[n / 2 - 1][0]
# print "b1, b2"
# print b1, b2
# print "caz [0, n]", trapezoidal_rule(points, a, b1, n)
# print "caz [0, n/2]", trapezoidal_rule(points, a, b2, n / 2)

ratio = trapezoidal_rule(points, a, b1, n) / (trapezoidal_rule(points, a, b2, n / 2))
# print ratio

if ratio < 2.1 and ratio > 2:
    print "O(1)"
elif ratio > 2.1 and ratio < 2.2:
    print "O(log n)"
elif ratio > 4 and ratio < 4.15:
    print "O(n)"
elif ratio > 4.15 and ratio < 5:
    print "O(n log n)"
elif ratio > 8 and ratio < 9:
    print "O(n^2)"
elif ratio > 7.5 and ratio < 8:
    print "O(n^2 log n)"
elif ratio > 16 and ratio < 18:
    print "O(n^3)"
else:
    print "O(2^n)"