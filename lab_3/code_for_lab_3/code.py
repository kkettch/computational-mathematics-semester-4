import math
import os
import random
import re
import sys

k = 0.4
a = 0.9

def first_function(args: []) -> float:
    return math.sin(args[0])

def second_function(args: []) -> float:
    return (args[0] * args[1]) / 2

def third_function(args: []) -> float:
    return math.tan(args[0]*args[1] + k) - pow(args[0], 2)

def fourth_function(args: []) -> float:
    return a * pow(args[0], 2) + 2 * pow(args[1], 2) - 1

def fifth_function(args: []) -> float:
    return pow(args[0], 2) + pow(args[1], 2) + pow(args[2], 2) - 1

def six_function(args: []) -> float:
    return 2 * pow(args[0], 2) + pow(args[1], 2) - 4 * args[2]

def seven_function(args: []) -> float:
    return 3 * pow(args[0], 2) - 4 * args[1] + pow(args[2], 2)

def default_function(args: []) -> float:
    return 0.0

def get_functions(n: int):
    if n == 1:
        return [first_function, second_function]
    elif n == 2:
        k = 0.4
        a = 0.9
        return [third_function, fourth_function]
    elif n == 3:
        k = 0
        a = 0.5
        return [third_function, fourth_function]
    elif n == 4:
        return [fifth_function, six_function, seven_function]
    else:
        return [default_function]

#решение СЛАУ методом Гаусса
class Solution:
    isSolutionExists = True
    errorMessage = ""

    # Функция для переставления строк при обнаружении нуля на главное диагонали
    def swap_lines(i, matrix):
        for k in range(i + 1, len(matrix)):
            if matrix[k][i] != 0:
                matrix[i], matrix[k] = matrix[k], matrix[i]
                return matrix
        return matrix

    # Функция для проверки существования решения СЛАУ
    def isSolvable(matrix):
        for row in matrix:
            # Проверка всех элементов кроме последнего (после знака равно)
            for coefficient in row[:-1]: 
                if coefficient != 0:
                    return True
        return False

    #Функция для решения СЛАУ методом Гаусса
    def solveByGauss(n, matrix): 

        # Создание копии матрицы
        matrix_copy = [row[:] for row in matrix]

        # Проверка на то, что количество неизвестных равно количеству уравнений
        for row in matrix:
            if len(row) != n + 1:
                Solution.isSolutionExists = False
                Solution.errorMessage = "The system has no roots of equations or has an infinite set of them."
                return

        # 1. Приведение матрицы к диагональному (треугольному) виду 
        for i in range(n):

            # 1.1 Если элемент на главной диагонали равен нулю, то необходимо поменять строки местами
            if matrix[i][i] == 0:
                matrix = Solution.swap_lines(i, matrix)
                if matrix[i][i] == 0:
                    Solution.isSolutionExists = False
                    Solution.errorMessage = "The system has no roots of equations or has an infinite set of them."
                    return
            
            # 1.2 После переставления высчитываем треугольную матрицу
            for j in range(i + 1, n):
                # Значение на которое умножаем все элементы следующих строк
                koef = matrix[j][i] / matrix[i][i]
                for k in range(i, n + 1):
                    matrix[j][k] = matrix[j][k] - koef * matrix[i][k]
        
        # 2. Проверка на возможность решения (если все коэффициенты в строке до знака равно обнулились, то решения не существует)
        if (Solution.isSolvable(matrix) == False):
            Solution.isSolutionExists = False
            Solution.errorMessage = "The system has no roots of equations or has an infinite set of them."
            return
        
        # 3. Нахождение корней уравнения обратным ходом 
        # Массив для хранения решений
        solution = [0] * n
        for i in range(n - 1, -1, -1):
            sum_koef = 0
            for j in range(i + 1, n):
                # Сумма коэффициентов в левой части уравнения
                sum_koef = sum_koef + matrix[i][j] * solution[j]
            solution[i] = round((matrix[i][-1] - sum_koef) / matrix[i][i], 5)

        # 5. Возвращение полученных значений неизвестных
        return solution

#частная производная
def partial_derivative(func, args: [], index, h=1e-6): 
    args_changed = args[:]
    args_changed[index] += h
    return ((func(args_changed) - func(args)) / h)

def solve_by_fixed_point_iterations(system_id, number_of_unknowns, initial_approximations):
    
    system_of_equations = get_functions(system_id)

    # Выполняем итерации метода Ньютона
    for _ in range(100):  # Максимальное количество итераций, чтобы избежать бесконечного цикла
        # Создаем матрицу Якоби
        jacobian_matrix = [[partial_derivative(func, initial_approximations, j) for j in range(number_of_unknowns)] for func in system_of_equations]

        # Создаем столбец значений функций
        functions_values = [-func(initial_approximations) for func in system_of_equations]

        # Решаем систему линейных уравнений методом Гаусса
        solution = Solution.solveByGauss(number_of_unknowns, [jacobian_matrix[i] + [functions_values[i]] for i in range(len(jacobian_matrix))])

        # Обновляем значения приближений
        for i in range(number_of_unknowns):
            initial_approximations[i] += solution[i]

        # Проверяем критерий останова
        if all(abs(func(initial_approximations)) < 1e-5 for func in system_of_equations):
            break

    return [round(approximation, 5) for approximation in initial_approximations]

                

if __name__ == '__main__':
    system_id = int(input().strip()) #k - номер системы

    number_of_unknowns = int(input().strip()) #n - кол-во неизвестных

    initial_approximations = []

    for _ in range(number_of_unknowns):
        initial_approximations_item = float(input().strip())
        initial_approximations.append(initial_approximations_item)

    result = solve_by_fixed_point_iterations(system_id, number_of_unknowns, initial_approximations)

    print('\n'.join(map(str, result)))
    print('\n')