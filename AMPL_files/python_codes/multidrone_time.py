import sys, numpy as np
from grid import display_path
from subprocess import Popen, PIPE
import imageio


grid_size = 10

time = 15

number_of_drones = 3

np.random.seed(1000)

obstacles_number = np.random.choice(np.arange(2 * grid_size + 1))

battery_swapping_stations_number = 2 * grid_size

points_choose = np.random.choice(np.arange(grid_size**2) + 1, 2 * number_of_drones + obstacles_number + battery_swapping_stations_number, replace=False)

initial_final_points_choose = np.random.choice(points_choose, 2 * number_of_drones, replace=False)
initial_final_points = []

for i in initial_final_points_choose:
    if i % grid_size == 0:
        initial_final_points.append(((i // grid_size), grid_size))
    else:
        initial_final_points.append((1 + (i // grid_size), (i % grid_size)))


obstacles_choose = np.random.choice(np.setdiff1d(points_choose, initial_final_points_choose), obstacles_number, replace=False)
obstacles = []

for i in obstacles_choose:
    if i % grid_size == 0:
        obstacles.append(((i // grid_size), grid_size))
    else:
        obstacles.append((1 + (i // grid_size), (i % grid_size)))


battery_swapping_stations_choose = np.random.choice(np.setdiff1d(np.setdiff1d(points_choose, initial_final_points_choose), obstacles_choose), battery_swapping_stations_number, replace=False)
battery_swapping_stations = []

for i in battery_swapping_stations_choose:
    if i % grid_size == 0:
        battery_swapping_stations.append(((i // grid_size), grid_size))
    else:
        battery_swapping_stations.append((1 + (i // grid_size), (i % grid_size)))


battery_added = np.zeros((grid_size + 2, grid_size + 2), dtype=int)

battery_swapping_stations_temp = []
for i in range(len(battery_swapping_stations)):
    battery_swapping_stations_temp.append((battery_swapping_stations[i][0] - 1, battery_swapping_stations[i][1] - 1))

initial_final_points_temp = []
for i in range(len(initial_final_points)):
    initial_final_points_temp.append((initial_final_points[i][0] - 1, initial_final_points[i][1] - 1))

obstacles_temp = []
for i in range(len(obstacles)):
    obstacles_temp.append((obstacles[i][0] - 1, obstacles[i][1] - 1))


for i in range(grid_size):
    for j in range(grid_size):
        if (((i, j) in battery_swapping_stations_temp) or ((i, j) in initial_final_points_temp)):
            battery_added[i + 1][j + 1] = 10


def CreateDatFile(datfile):
    original_stdout = sys.stdout

    with open(datfile, 'w') as file:
        sys.stdout = file

        print(f'param grid_size := {grid_size + 2};')
        print(f'param time := {time};')
        print(f'param number_of_drones := {number_of_drones};')
        print(f'param obstacles_number := {obstacles_number};')
        print(f'param battery_swapping_stations_number := {battery_swapping_stations_number + 2 * number_of_drones};')
        print(f'param initial_final_points :=')
        for i in range(2 * number_of_drones):
            print(f'{2 * i + 1} {initial_final_points[i][0] + 1}')
            print(f'{2 * i + 2} {initial_final_points[i][1] + 1}')
        print(';')
        print('param obstacles :=')
        for i in range(obstacles_number):
            print(f'{2 * i + 1} {obstacles[i][0] + 1}')
            print(f'{2 * i + 2} {obstacles[i][1] + 1}')
        print(';')
        print('param battery_swapping_stations :=')
        for i in range(battery_swapping_stations_number):
            print(f'{2 * i + 1} {battery_swapping_stations[i][0] + 1}')
            print(f'{2 * i + 2} {battery_swapping_stations[i][1] + 1}')
        for i in range(2 * number_of_drones):
            print(f'{2 * (battery_swapping_stations_number + i) + 1} {initial_final_points[i][0] + 1}')
            print(f'{2 * (battery_swapping_stations_number + i) + 2} {initial_final_points[i][1] + 1}')
        print(';')
        print(f'param battery_added\n: ', end='')
        for i in range(1, grid_size + 3):
            print(f'{i} ', end='')
        print(':=')
        for i in range(grid_size + 2):
            print(i + 1, *battery_added[i])
        print(';')
        '''print('param distance_matrix :=')
        for i in range(grid_size + 2):
            for j in range(grid_size + 2):
                print(f'[{i + 1}, {j + 1}, *, *]: ', end='')
                for k in range(1, grid_size + 3):
                    print(f'{k} ', end='')
                print(':=')
                for l in range(grid_size + 2):
                    print(l + 1, *distance_matrix[i][j][l])
        print(';')'''
        
        sys.stdout = original_stdout


def RunAMPLFromPython(runfile):
    pathToamplExe = r'C:/Users/saayu/Downloads/amplbundle.mswin64/ampl.mswin64/ampl'
    pathToRunFile = runfile

    process = Popen([pathToamplExe, pathToRunFile], stdin=PIPE, stdout=PIPE)

    for line in process.stdout:
        print(line, end="")
        print('\n')


def ProcessAMPLOutput(nodesfile, bsvfile):
    with open(nodesfile) as file:
        nodes_string = file.readlines()

    nodes_temp = np.zeros((time, number_of_drones, grid_size, grid_size), dtype=int)

    for i in range(time):
        for j in range(number_of_drones):
            nodes_temp[i][int(nodes_string[6 * i + j + 1].split()[0]) - 1][int(nodes_string[6 * i + j + 1].split()[1]) - 2][int(nodes_string[6 * i + j + 1].split()[2]) - 2] = 1


    with open(bsvfile) as file:
        battery_stations_visited_string = file.readlines()

    battery_stations_visited_temp = np.zeros((time, number_of_drones, grid_size, grid_size), dtype=int)

    for i in range(time):
            for j in range(number_of_drones):
                    for k in range(grid_size):
                            for l in range(grid_size):
                                    battery_stations_visited_temp[i][j][k][l] = battery_stations_visited_string[46 * i + 15 * j + k + 3].split()[l + 2]


    nodes = np.zeros((grid_size, grid_size), dtype=int)
    frames = []

    for i in range(time):
            for j in range(number_of_drones):
                    for k in range(grid_size):
                            for l in range(grid_size):
                                    if (k, l) in obstacles_temp:
                                        nodes[k][l] = 5
                                    else:
                                        if nodes_temp[i][j][k][l] == 1:
                                            nodes[k][l] = j + 2
                                        else:
                                            if (k, l) in battery_swapping_stations_temp:
                                                nodes[k][l] = 6

            display_path(nodes, i)

            image = imageio.v2.imread(f'grid{i}.png')
            frames.append(image)


    imageio.mimsave('grid.gif', frames, fps = 1)

    # nodes = np.zeros((grid_size, grid_size), dtype=int)

    # for i in range(grid_size):
    #     for j in range(grid_size):
    #         if (i, j) in initial_final_points_temp:
    #             nodes[i][j] = 3
    #         else:
    #             if (i, j) in obstacles_temp:
    #                 nodes[i][j] = 4
    #             else:
    #                 if (i, j) in battery_swapping_stations_temp:
    #                     nodes[i][j] = 5
    #             if battery_stations_visited_temp[i][j] == 1:
    #                 nodes[i][j] = 6
    #         if nodes_temp[i][j] == 1 and battery_stations_visited_temp[i][j] != 1:
    #             nodes[i][j] = 2


    # display_path(nodes)


CreateDatFile('multidrone_time.dat')
RunAMPLFromPython('multidrone_time.run')
ProcessAMPLOutput('nodes.txt', 'battery_stations_visited.txt')
