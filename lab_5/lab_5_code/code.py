import math
import os
import random
import re
import sys

class Result:
    
    def first_function(x: float, y: float):
        return math.sin(x)


    def second_function(x: float, y: float):
        return (x * y)/2


    def third_function(x: float, y: float):
        return y - (2 * x)/y


    def fourth_function(x: float, y: float):
        return x + y

    
    def default_function(x:float, y: float):
        return 0.0

    # How to use this function:
    # func = Result.get_function(4)
    # func(0.01)
    def get_function(n: int):
        if n == 1:
            return Result.first_function
        elif n == 2:
            return Result.second_function
        elif n == 3:
            return Result.third_function
        elif n == 4:
            return Result.fourth_function
        else:
            return Result.default_function

    #
    # Complete the 'solveByEulerImproved' function below.
    #
    # The function is expected to return a DOUBLE.
    # The function accepts following parameters:
    #  1. INTEGER f
    #  2. DOUBLE epsilon
    #  3. DOUBLE a
    #  4. DOUBLE y_a
    #  5. DOUBLE b
    #
    def solveByEulerImproved(f, epsilon, a, y_a, b):

        func = Result.get_function(f)
        h = (b - a) / (1 / epsilon)
        x_i = a
        y_i = y_a

        while (x_i < b):
            
            delta_y = h * func(x_i + h / 2, y_i + (h / 2) * func(x_i, y_i))
            y_new = y_i + delta_y

            x_i = x_i + h
            y_i = y_new

        return y_i


if __name__ == '__main__':
    f = int(input().strip())

    epsilon = float(input().strip())

    a = float(input().strip())

    y_a = float(input().strip())

    b = float(input().strip())

    result = Result.solveByEulerImproved(f, epsilon, a, y_a, b)

    print(str(result) + '\n')
