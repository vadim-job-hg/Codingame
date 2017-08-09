import sys
import math

SYSTEM_SS = 20


class CalculateMaya:
    numerals = {}
    num_1line = {}
    num_2line = {}
    operation = None

    def __init__(self):
        l, h = [int(i) for i in input().split()]
        self.numerals = {i: list() for i in range(SYSTEM_SS)}
        for i in range(h):
            numeral = input()
            for j in range(0, len(numeral), l):
                num = self.numerals[int(j / l)].append(numeral[j:j + l])

        print(self.numerals, file=sys.stderr)
        s1 = int(input())
        self.num_1line = {i: list() for i in range(int(s1 / h))}
        for i in range(s1):
            # print(s1, i, h, file=sys.stderr)
            self.num_1line[math.floor((s1 - i - 1) / h)].append(input())
        print(self.num_1line, file=sys.stderr)
        s2 = int(input())
        self.num_2line = {i: list() for i in range(int(s2 / h))}
        for i in range(s2):
            self.num_2line[math.floor((s2 - i - 1) / h)].append(input())
        print(self.num_2line, file=sys.stderr)
        self.operation = input()

    def calculate(self):
        num1 = num2 = 0
        for key, value in self.num_1line.items():
            num1 += self.get_numeral(value) * (20 ** key)
        print(num1, file=sys.stderr)
        for key, value in self.num_2line.items():
            num2 += self.get_numeral(value) * (20 ** key)
        print(num2, file=sys.stderr)
        result = int(self._make_operation(num1, num2))
        self._out(result)

    def _make_operation(self, num1, num2):
        print(self.operation, file=sys.stderr)
        if self.operation == "+":
            return num1 + num2
        elif self.operation == "*":
            return num1 * num2
        elif self.operation == "-":
            return num1 - num2
        elif self.operation == "/":
            return math.ceil(num1 / num2)

    def get_numeral(self, value0):
        for key, value in self.numerals.items():
            if value == value0:
                # print("got {0}".format(key), file=sys.stderr)
                return key
        return 0

    def get_ASCII(self, key0):
        for key, value in self.numerals.items():
            if key == key0:
                # print("got {0}".format(value), file=sys.stderr)
                return value
        raise Error('HiThere')

    def _out(self, result):
        temp_array = []
        print("result {0}".format(result), file=sys.stderr)
        result_20 = []
        if result > 0:
            while result > 0:
                num = math.floor(result % 20)
                result_20.append(num)
                result = math.floor(result / 20)
                print("num {0} left {1}".format(num, result), file=sys.stderr)
                temp = self.get_ASCII(num)
                print("temp {0}".format(temp), file=sys.stderr)
                temp.extend(temp_array)
                temp_array = temp
        print("result_20 {0}".format(result_20), file=sys.stderr)
        i = 0
        for item in temp_array:
            if i % 4 == 0 or i == 0:
                print("NUM {0}".format(result_20[-(math.floor(i / 4) - 1)]), file=sys.stderr)
                i += 1
                print("{0}".format(item), file=sys.stderr)
                print("{0}".format(item))
                if i == 125:
                    print("oooo".format(item))
                    print("oooo".format(item))
                    return

# 7c3h42h0
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
calc = CalculateMaya()
calc.calculate()


