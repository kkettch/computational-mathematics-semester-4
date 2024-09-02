import math
import os
import random
import re
import sys

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

    # Функция для рассчета невязок
    def calculationOfResiduals(matrix, solution, n):

        for i in range(n):
            sum_of_left_part = 0
            for j in range(n):
                # Подсчет значений левой части уравнения
                sum_of_left_part += matrix[i][j] * solution[j]
            # Вычисление невязки
            solution[n + i] = matrix[i][-1] - round(sum_of_left_part, 10)
        return solution

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
        solution = [0] * n * 2
        for i in range(n - 1, -1, -1):
            sum_koef = 0
            for j in range(i + 1, n):
                # Сумма коэффициентов в левой части уравнения
                sum_koef = sum_koef + matrix[i][j] * solution[j]
            solution[i] = (matrix[i][-1] - sum_koef) / matrix[i][i]
        
        # 4. Рассчет невязок 
        Solution.calculationOfResiduals(matrix_copy, solution, n)

        # 5. Возвращение полученных значений неизвестных
        return solution

if __name__ == '__main__':
    n = int(input().strip())

    matrix_rows = n
    matrix_columns = n + 1

    matrix = []

    for _ in range(matrix_rows):
        matrix.append(list(map(float, input().rstrip().split())))

    result = Solution.solveByGauss(n, matrix)
    if Solution.isSolutionExists:
        print('\n'.join(map(str, result)))
    else:
        print(f"{Solution.errorMessage}")
    print("")