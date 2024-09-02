import math
import os
import random
import re
import sys

class Result:
    error_message = ""
    has_discontinuity = False
    
    def first_function(x: float):
        return 1 / x


    def second_function(x: float):
        if x == 0:
            return (math.sin(Result.eps)/Result.eps + math.sin(-Result.eps)/-Result.eps)/2 
        return math.sin(x)/x


    def third_function(x: float):
        return x*x+2


    def fourth_function(x: float):
        return 2*x+2


    def five_function(x: float):
        return math.log(x)
    
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
        elif n == 5:
            return Result.five_function
        else:
            raise NotImplementedError(f"Function {n} not defined.")

    def calculate_integral(a, b, f, epsilon):

        if (f == 1) and (a <= 0 <= b):
            Result.error_message = "Integrated function has discontinuity or does not defined in current interval"
            Result.has_discontinuity = True
            return 
        
        if (f == 5) and (min(a, b) < 0):
            Result.error_message = "Integrated function has discontinuity or does not defined in current interval"
            Result.has_discontinuity = True
            return

        function_to_integrate = Result.get_function(f) # определяем функцию, которую будет интегрировать
        n = 4 # количество отрезков разбиения 
        previous_integral = None

        while True: 
            
            h = (max(a, b) - min(a, b)) / n # шаг разбиения 

            function_value_array = [] # массив для хранения значений функций при разных шагах

            # заполнение массива значениями функции 
            for i in range (n):
                value = min(a, b) + i * h

                if (f == 2) and (value == 0):
                    function_value_array.append(1)

                elif (f == 5) and (value == 0):
                    function_value_array.append(0)

                else:
                    function_value_array.append(function_to_integrate(value))

            # сумма значений функции с нечетными и четными индексами (кроме крайних)
            sum_of_odd = 0
            sum_of_even = 0

            first_element = function_value_array[0]
            last_element = function_value_array[n - 1]

            #вычисления сумм
            for i in range(1, n-1):
                if (i % 2 == 0):
                    sum_of_even += function_value_array[i]
                else:
                    sum_of_odd += function_value_array[i]

            # вычисление интеграла 
            integral_of_sympsons = (h / 3) * (first_element + last_element + 4 * (sum_of_odd) + 2 * (sum_of_even))

            if (previous_integral != None):
                if (abs(integral_of_sympsons - previous_integral)) <= epsilon:
                    break

            previous_integral = integral_of_sympsons
            n *= 2
        
        if (a > b):
            integral_of_sympsons *= -1
        
        return integral_of_sympsons


if __name__ == '__main__':

    a = float(input().strip())

    b = float(input().strip())

    f = int(input().strip())

    epsilon = float(input().strip())

    result = Result.calculate_integral(a, b, f, epsilon)

    if Result.has_discontinuity == False:
        print(str(result) + '\n')
    else:
        print(Result.error_message + '\n')
