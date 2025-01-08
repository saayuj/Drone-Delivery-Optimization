import sys, numpy as np

grid_size = 10

cost_per_hop = -5

battery_swapping_stations_number = 20

points_choose = np.random.choice(np.arange(grid_size**2) + 1, 2 + battery_swapping_stations_number, replace=False)

initial_final_points_choose = np.random.choice(points_choose, 2, replace=False)
initial_final_points = []

for i in initial_final_points_choose:
    if i % 10 == 0:
        initial_final_points.append(((i // 10), 10))
    else:
        initial_final_points.append((1 + (i // 10), (i % 10)))


battery_swapping_stations_choose = np.random.choice(np.setdiff1d(points_choose, initial_final_points_choose), battery_swapping_stations_number, replace=False)
battery_swapping_stations = []

for i in battery_swapping_stations_choose:
    if i % 10 == 0:
        battery_swapping_stations.append(((i // 10), 10))
    else:
        battery_swapping_stations.append((1 + (i // 10), (i % 10)))


battery_added = np.zeros((10, 10), dtype=int)

battery_swapping_stations_temp = []
for i in range(len(battery_swapping_stations)):
    battery_swapping_stations_temp.append((battery_swapping_stations[i][0] - 1, battery_swapping_stations[i][1] - 1))

initial_final_points_temp = []
for i in range(len(initial_final_points)):
    initial_final_points_temp.append((initial_final_points[i][0] - 1, initial_final_points[i][1] - 1))


for i in range(10):
    for j in range(10):
        if (((i, j) in battery_swapping_stations_temp) or ((i, j) in initial_final_points_temp)):
            battery_added[i][j] = 10


original_stdout = sys.stdout

with open('trajectory_bss.dat', 'w') as file:
    sys.stdout = file

    print(f'param grid_size := {grid_size};')
    print(f'param cost_per_hop := {cost_per_hop};')
    print(f'param battery_swapping_stations_number := {battery_swapping_stations_number};')
    print(f'param initial_final_points :=\n1 {initial_final_points[0][0]}\n2 {initial_final_points[0][1]}\n3 {initial_final_points[1][0]}\n4 {initial_final_points[1][1]}\n;')
    print('param battery_swapping_stations :=')
    for i in range(battery_swapping_stations_number):
        print(f'{2 * i + 1} {battery_swapping_stations[i][0]}')
        print(f'{2 * i + 2} {battery_swapping_stations[i][1]}')
    print(';')
    print(f'param battery_added\n: 1 2 3 4 5 6 7 8 9 10 :=')
    for i in range(10):
        print(i + 1, *battery_added[i])
    print(';')

    sys.stdout = original_stdout
