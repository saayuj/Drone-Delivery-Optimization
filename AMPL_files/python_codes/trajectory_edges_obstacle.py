import sys, numpy as np
from grid import display_path


grid_size = 10

np.random.seed(10000)

obstacles_number = np.random.choice(np.arange(11))

points_choose = np.random.choice(np.arange(grid_size**2) + 1, 2 + obstacles_number, replace=False)

initial_final_points_choose = np.random.choice(points_choose, 2, replace=False)
initial_final_points = []

for i in initial_final_points_choose:
    if i % 10 == 0:
        initial_final_points.append(((i // 10), 10))
    else:
        initial_final_points.append((1 + (i // 10), (i % 10)))


obstacles_choose = np.random.choice(np.setdiff1d(points_choose, initial_final_points_choose), obstacles_number, replace=False)
obstacles = []

for i in obstacles_choose:
    if i % 10 == 0:
        obstacles.append(((i // 10), 10))
    else:
        obstacles.append((1 + (i // 10), (i % 10)))


distance_matrix = np.zeros((grid_size, grid_size, grid_size, grid_size))

for i in range(grid_size):
    for j in range(grid_size):
        for k in range(grid_size):
            for l in range(grid_size):
                if (k, l) == (i, j - 1) or (k, l) == (i, j + 1) or (k, l) == (i - 1, j) or (k, l) == (i + 1, j):
                    distance_matrix[i][j][k][l] = 1
                elif (k, l) == (i - 1, j - 1) or (k, l) == (i - 1, j + 1) or (k, l) == (i + 1, j - 1) or (k, l) == (i + 1, j + 1):
                    distance_matrix[i][j][k][l] = 1.4142
                else:
                    distance_matrix[i][j][k][l] = 0


initial_final_points_temp = []
for i in range(len(initial_final_points)):
    initial_final_points_temp.append((initial_final_points[i][0] - 1, initial_final_points[i][1] - 1))

obstacles_temp = []
for i in range(len(obstacles)):
    obstacles_temp.append((obstacles[i][0] - 1, obstacles[i][1] - 1))


original_stdout = sys.stdout

with open('trajectory_obstacle.dat', 'w') as file:
    sys.stdout = file

    print(f'param grid_size := {grid_size};')
    print(f'param obstacles_number := {obstacles_number};')
    print(f'param initial_final_points :=\n1 {initial_final_points[0][0]}\n2 {initial_final_points[0][1]}\n3 {initial_final_points[1][0]}\n4 {initial_final_points[1][1]}\n;')
    print('param obstacles :=')
    for i in range(obstacles_number):
        print(f'{2 * i + 1} {obstacles[i][0]}')
        print(f'{2 * i + 2} {obstacles[i][1]}')
    print(';')
    print('param distance_matrix :=')
    for i in range(grid_size):
        for j in range(grid_size):
            print(f'[{i + 1}, {j + 1}, *, *]: 1 2 3 4 5 6 7 8 9 10 :=')
            for k in range(grid_size):
                print(k + 1, *distance_matrix[i][j][k])
    print(';')

    sys.stdout = original_stdout


with open('nodes.txt') as file:
    nodes_string = file.readlines()

nodes_temp = np.zeros((grid_size, grid_size), dtype=int)

for i in range(grid_size):
    for j in range(grid_size):
        nodes_temp[i][j] = nodes_string[i + 2].split()[j + 1]


nodes = np.zeros((grid_size, grid_size), dtype=int)

for i in range(grid_size):
    for j in range(grid_size):
        if (i, j) in initial_final_points_temp:
            nodes[i][j] = 3
        else:
            if (i, j) in obstacles_temp:
                    nodes[i][j] = 4
            else:
                if nodes_temp[i][j] == 1:
                    nodes[i][j] = 2


display_path(nodes)
