# adapted from https://github.com/aethersg/codingame-puzzle/blob/master/Python/hard/Bender-Episode%203.py
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

algo_names = ["1", "log n", "n", "n log n", "n^2", "n^2 log n", "n^3", "2^n"]
complex = [lambda x: 1,
           lambda x: math.log(x),
           lambda x: x,
           lambda x: x * math.log(x),
           lambda x: x ** 2,
           lambda x: x ** 2 * math.log(x),
           lambda x: x ** 3,
           lambda x: math.pow(2, x)]

upperLimit = [None, None, None, None, None, None, None, 500]

x, pref = [], []
n = int(input())
for i in range(n):
    num, t = [int(j) for j in input().split()]
    x.append(num)
    pref.append(t)    

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

variances, minVariance, result = [], sys.maxsize, -1

for i in range(len(complex)):
    f = complex[i]
    # takes upperLimit into account to avoid an overflow
    maxDataVolume = len(x)
    if upperLimit[i] is not None:
        for j in range(len(x)):
            if x[j] > upperLimit[i]:
                maxDataVolume = j - 1
                break

    ratio = [pref[j] / f(x[j]) for j in range(maxDataVolume)]
    if len(ratio) < 5:
        variances.append(-1)
    else:
        mean = sum(ratio) / len(ratio)
        variances.append(sum([(val - mean) ** 2 for val in ratio]) / mean ** 2)
        if variances[-1] < minVariance:
            minVariance = variances[-1]
            result = i

print("O({})".format(algo_names[result]))