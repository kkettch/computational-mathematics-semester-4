import math
import os
import random
import re
import sys
def interpolate_by_spline(x_axis, y_axis, x):
    length = len(x_axis)
    inner_length = (length - 1) * 4 + 1
    array_of_arrays = [[] for _ in range(inner_length - 1)]
    for i in range(inner_length - 1):
        array_of_arrays[i] = [0] * inner_length
    x_definition = 0
    x_i_definition = 0
    for i in range((length - 1) * 2):
        if (i % 2 == 0):
            x_definition = int(i / 2)
        else:
            x_i_definition += 1
        array_of_arrays[i][4 * x_definition + 0] = 1.0
        for j in range(1, 4):
            array_of_arrays[i][4 * x_definition + j] = (x_axis[x_i_definition] - x_axis[x_definition]) ** j
        array_of_arrays[i][inner_length - 1] = y_axis[x_i_definition]    
    x_definition = 0
    for i in range((length - 1) * 2, inner_length - 1 - 2):
        if (i % 2 == 0):
            array_of_arrays[i][4 * x_definition + 1] = 1.0
            array_of_arrays[i][4 * x_definition + 2] = 2 * (x_axis[x_definition + 1] - x_axis[x_definition])
            array_of_arrays[i][4 * x_definition + 3] = 3 * (x_axis[x_definition + 1] - x_axis[x_definition]) ** 2
            array_of_arrays[i][4 * (x_definition + 1) + 1] = -1.0
        else:
            array_of_arrays[i][4 * x_definition + 2] = 2.0
            array_of_arrays[i][4 * x_definition + 3] = 6 * (x_axis[x_definition + 1] - x_axis[x_definition])
            array_of_arrays[i][4 * (x_definition + 1) + 2] = -2.0
            x_definition += 1    
    array_of_arrays[inner_length - 1 - 2][4 * 0 + 2] = 2.0    
    array_of_arrays[inner_length - 1 - 1][4 * (length - 2) + 2] = 2.0
    array_of_arrays[inner_length - 1 - 1][4 * (length - 2) + 3] = 6 * (x_axis[length - 1] - x_axis[length - 2])
    result_matrix = gaussian_elimination(array_of_arrays)
    return function_value(x_axis, result_matrix, x)
def function_value(x_axis, result_matrix, x):
    for i in range(len(x_axis) - 1):
        if x >= x_axis[i] and x <= x_axis[i + 1]:
            x_0 = x_axis[i]
            return result_matrix[4 * i + 0] + result_matrix[4 * i + 1] * (x - x_0) + result_matrix[4 * i + 2] * (x - x_0) ** 2 + result_matrix[4 * i + 3] * (x - x_0) ** 3
    return "Wrong X"
def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) - 1 
    for i in range(min(rows, cols)): 
        max_row = max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i + 1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, cols + 1):
                matrix[j][k] -= factor * matrix[i][k]
    for i in range(rows - 1, -1, -1):
        for j in range(i + 1, rows):
            matrix[i][cols] -= matrix[j][cols] * matrix[i][j]
        matrix[i][cols] /= matrix[i][i]
        
    return [row[cols] for row in matrix]


matrix = [
    [4, 1, 2, 2],
    [2, 3, -1, 1],
    [1, -2, 1, 3]
]
gaussian_elimination(matrix)

axis_count = int(input().strip())
x_axis = list(map(float, input().rstrip().split()))
y_axis = list(map(float, input().rstrip().split()))
x = float(input().strip())
result = interpolate_by_spline(x_axis, y_axis, x)
print(str(result) + '\n')