import sys
import math
import copy

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
                self.numerals[int(j / l)].append(numeral[j:j + l])

        s1 = int(input())
        self.num_1line = {i: list() for i in range(int(s1 / h))}
        for i in range(s1):
            self.num_1line[math.floor((s1 - i - 1) / h)].append(input())
        s2 = int(input())
        self.num_2line = {i: list() for i in range(int(s2 / h))}
        for i in range(s2):
            self.num_2line[math.floor((s2 - i - 1) / h)].append(input())
        self.operation = input()

    def calculate(self):
        num1 = num2 = 0
        for key, value in self.num_1line.items():
            num1 += self.get_numeral(value) * (20 ** key)
        for key, value in self.num_2line.items():
            num2 += self.get_numeral(value) * (20 ** key)
        result = int(self._make_operation(num1, num2))
        self._out(result)

    def _make_operation(self, num1, num2):
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
                return key
        return Exception('HiThere')

    def get_ASCII(self, key0):
        for key, ascii in self.numerals.items():
            if key == key0:
                return copy.copy(ascii)
        raise Exception('HiThere')

    def _out(self, result):
        temp_array = []
        result_20 = []
        if result > 0:
            while result > 0:
                num = result % 20
                result_20.append(num)
                result = math.floor(result / 20)
                temp = self.get_ASCII(num)
                temp.extend(temp_array)
                temp_array = temp
        else:
            temp_array = self.get_ASCII(0)

        i = 0
        for item in temp_array:
            i += 1
            print("{0}".format(item))
calc = CalculateMaya()
calc.calculate()


