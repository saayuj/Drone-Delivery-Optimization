import sys, numpy as np

grid_size = 10

initial_final_points_choose = np.random.choice(np.arange(grid_size**2) + 1, 2, replace=False)
initial_final_points = []

for i in initial_final_points_choose:
    if i % 10 == 0:
        initial_final_points.append(((i // 10), 10))
    else:
        initial_final_points.append((1 + (i // 10), (i % 10)))


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


original_stdout = sys.stdout

with open('trajectory.dat', 'w') as file:
    sys.stdout = file

    print(f'param grid_size := {grid_size};')
    print(f'param initial_final_points :=\n1 {initial_final_points[0][0]}\n2 {initial_final_points[0][1]}\n3 {initial_final_points[1][0]}\n4 {initial_final_points[1][1]}\n;')
    print('param distance_matrix :=')
    for i in range(grid_size):
        for j in range(grid_size):
            print(f'[{i + 1}, {j + 1}, *, *]: 1 2 3 4 5 6 7 8 9 10 :=')
            for k in range(grid_size):
                print(k + 1, *distance_matrix[i][j][k])
    print(';')

    sys.stdout = original_stdout
