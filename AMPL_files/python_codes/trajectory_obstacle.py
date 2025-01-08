import sys, numpy as np

grid_size = 10

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
    
    sys.stdout = original_stdout
