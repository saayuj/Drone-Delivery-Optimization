import sys, numpy as np
from grid2 import display_path
from subprocess import Popen, PIPE
import imageio


grid_size = 10

time = 20

number_of_drones = 3


with open('nodes.txt') as file:
        nodes_string = file.readlines()

nodes_temp = np.zeros((time, number_of_drones, grid_size, grid_size), dtype=int)

for i in range(time):
    for j in range(number_of_drones):
        nodes_temp[i][int(nodes_string[6 * i + j + 1].split()[0]) - 1][int(nodes_string[6 * i + j + 1].split()[1]) - 2][int(nodes_string[6 * i + j + 1].split()[2]) - 2] = 1

with open('battery_stations_visited.txt') as file:
        battery_stations_visited_string = file.readlines()
        # battery_stations_visited_string = file.read()

battery_stations_visited_temp = np.zeros((time, number_of_drones, grid_size, grid_size), dtype=int)

for i in range(time):
        for j in range(number_of_drones):
                for k in range(grid_size):
                        for l in range(grid_size):
                                battery_stations_visited_temp[i][j][k][l] = battery_stations_visited_string[46 * i + 15 * j + k + 3].split()[l + 2]

print(battery_stations_visited_temp[19][2])
                                        # print(battery_stations_visited_string[46 * i + 15 * j + k + 3].split()[2:11])
                # for j in range(number_of_drones):
                #         print(battery_stations_visited_string[0])

        # battery_stations_visited_temp = np.zeros((grid_size, grid_size), dtype=int)

        # for i in range(grid_size):
        #         for j in range(grid_size):
        #                 battery_stations_visited_temp[i][j] = int(float(battery_stations_visited_string[i + 2].split()[j + 1]))


nodes = np.zeros((grid_size, grid_size), dtype=int)
frames = []

for i in range(time):
        for j in range(number_of_drones):
                for k in range(grid_size):
                        for l in range(grid_size):
                                if nodes_temp[i][j][k][l] == 1:
                                     nodes[k][l] = j + 2

        display_path(nodes, i)

        image = imageio.v2.imread(f'grid{i}.png')
        frames.append(image)


imageio.mimsave('grid.gif', frames, fps = 5)
