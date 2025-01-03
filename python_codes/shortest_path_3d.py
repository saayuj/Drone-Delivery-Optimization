import random
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from grid_shortest_path_3d import display_path_3d



# Create the required parameters
## Change input parameter values here only
grid_size = 10

np.random.seed(378) # 10, 378, 968, 1090 works # check 4, 555

obstacles_number = int(np.random.randint(10, 2 * grid_size + 1, size=1))

obstacles_choose = np.random.choice(np.arange(grid_size ** 2), obstacles_number, replace=False)

obstacles_height = np.random.randint(1, grid_size, size=obstacles_number)

obstacles = []

for i in range(obstacles_number):
        for j in np.arange(obstacles_height[i]):
            obstacles.append(((obstacles_choose[i] // grid_size) + 1, (obstacles_choose[i] % grid_size) + 1, j + 1))


battery_charging_stations_number = 2 * grid_size

battery_charging_stations_choose = np.random.choice(np.setdiff1d(np.arange(grid_size ** 2), obstacles_choose), battery_charging_stations_number - obstacles_number, replace=False)

battery_charging_stations = []

for i in battery_charging_stations_choose:
    battery_charging_stations.append(((i // grid_size) + 1, (i % grid_size) + 1, 1))

for i in range(obstacles_number):
    battery_charging_stations.append(((obstacles_choose[i] // grid_size) + 1, (obstacles_choose[i] % grid_size) + 1, obstacles_height[i] + 1))


initial_final_points_choose_2d = np.setdiff1d(np.setdiff1d(np.arange(grid_size ** 2), obstacles_choose), battery_charging_stations_choose)

initial_final_points_choose = []

for i in initial_final_points_choose_2d:
    initial_final_points_choose.append(((i // grid_size) + 1, (i % grid_size) + 1, 1))

initial_final_points_choose = initial_final_points_choose + battery_charging_stations

initial_final_points = random.sample(initial_final_points_choose, 2)


initial_final_points = [(10, 10, 10), (4, 4, 6)]


battery_added = np.zeros((grid_size + 2, grid_size + 2, grid_size + 2), dtype=int)

for i in range(grid_size + 2):
    for j in range(grid_size + 2):
        for k in range(grid_size + 2):
            if (((i, j, k) in battery_charging_stations) or ((i, j) in initial_final_points)):
                battery_added[i][j][k] = 1


distance_matrix = np.zeros((grid_size + 2, grid_size + 2, grid_size + 2, grid_size + 2, grid_size + 2, grid_size + 2))

for i in range(grid_size + 2):
    for j in range(grid_size + 2):
        for k in range(grid_size + 2):
            for l in range(grid_size + 2):
                for m in range(grid_size + 2):
                    for n in range(grid_size + 2):
                        if (l, m, n) == (i - 1, j, k) or (l, m, n) == (i + 1, j, k) or (l, m, n) == (i, j - 1, k) or (l, m, n) == (i, j + 1, k) or (l, m, n) == (i, j, k - 1) or (l, m, n) == (i, j, k + 1):
                            distance_matrix[i][j][k][l][m][n] = 1
                        elif (l, m, n) == (i - 1, j - 1, k) or (l, m, n) == (i - 1, j + 1, k) or (l, m, n) == (i + 1, j - 1, k) or (l, m, n) == (i + 1, j + 1, k) or (l, m, n) == (i - 1, j, k - 1) or (l, m, n) == (i - 1, j, k + 1) or (l, m, n) == (i + 1, j, k - 1) or (l, m, n) == (i + 1, j, k + 1) or (l, m, n) == (i, j - 1, k - 1) or (l, m, n) == (i, j - 1, k + 1) or (l, m, n) == (i, j + 1, k - 1) or (l, m, n) == (i, j + 1, k + 1):
                            distance_matrix[i][j][k][l][m][n] = 1.4142
                        elif (l, m, n) == (i - 1, j - 1, k - 1) or (l, m, n) == (i - 1, j - 1, k + 1) or (l, m, n) == (i - 1, j + 1, k - 1) or (l, m, n) == (i - 1, j + 1, k + 1) or (l, m, n) == (i + 1, j - 1, k - 1) or (l, m, n) == (i + 1, j - 1, k + 1) or (l, m, n) == (i + 1, j + 1, k - 1) or (l, m, n) == (i + 1, j + 1, k + 1):
                            distance_matrix[i][j][k][l][m][n] = 1.7321


bool_initial_final_points = np.zeros((grid_size + 2, grid_size + 2, grid_size + 2), dtype=int)

for i in range(grid_size + 2):
    for j in range(grid_size + 2):
        for k in range(grid_size + 2):
            if (i, j, k) in initial_final_points:
                bool_initial_final_points[i][j][k] = 1



# Create a new model
m = gp.Model('shortest_path')


# Create decision variables
nodes = m.addMVar((grid_size + 2, grid_size + 2, grid_size + 2), vtype=GRB.BINARY, name='nodes')
# battery_charging_stations_visited = m.addMVar((grid_size + 2, grid_size + 2, grid_size + 2), vtype=GRB.BINARY, name='battery_charging_stations_visited')


# Set objective function
m.setObjective(gp.quicksum(distance_matrix[i][j][k][l][m][n] * nodes[i, j, k] * nodes[l, m, n] for i in range(1, grid_size + 1) for j in range(1, grid_size + 1) for k in range(1, grid_size + 1) for l in range(1, grid_size + 1) for m in range(1, grid_size + 1) for n in range(1, grid_size + 1)) / 2, GRB.MINIMIZE)


# Add constraints
## Constraint 1 - Initial and final points should be 1
m.addConstrs((nodes[initial_final_points[i][0], initial_final_points[i][1], initial_final_points[i][2]] - 1 == 0 for i in range(2)), name='c0')

## Constraint 2 - Obstacles should be 0
m.addConstrs((nodes[obstacles[i][0], obstacles[i][1], obstacles[i][2]] == 0 for i in range(obstacles_number)), name='c1')

## Constraint 3 - Padded points should be 0
m.addConstrs((nodes[i, j, k] == 0 for i in range(grid_size + 2) for j in range(grid_size + 2) for k in [0, grid_size + 1]), name='c2')
m.addConstrs((nodes[i, j, k] == 0 for i in range(grid_size + 2) for j in [0, grid_size + 1] for k in range(1, grid_size + 1)), name='c2')
m.addConstrs((nodes[i, j, k] == 0 for i in [0, grid_size + 1] for j in range(1, grid_size + 1) for k in range(1, grid_size + 1)), name='c2')

## Constraint 4 - Define battery_charging_stations_visited as intersection of visited points & battery_charging_stations
# m.addConstrs((battery_charging_stations_visited[i, j, k] - battery_added[i][j][k] * nodes[i, j, k] ==  0 for i in range(grid_size + 2) for j in range(grid_size + 2) for k in range(grid_size + 2)), name='c3')

## Constraint 5 - Path should be connected
m.addConstrs((nodes[i, j, k] * (gp.quicksum(nodes[l, m, n] for l in [i - 1, i, i + 1] for m in [j - 1, j, j + 1] for n in [k - 1, k, k + 1]) + bool_initial_final_points[i][j][k] - 3) == 0 for i in range(1, grid_size + 1) for j in range(1, grid_size + 1) for k in range(1, grid_size + 1)), name='c4')

## Constraint 6 - Battery level should be positive at each hop (have considered maximum possible hops as two)
# m.addConstrs((gp.quicksum(battery_charging_stations_visited[l, m, n] for l in [i - 1, i, i + 1] for m in [j - 1, j, j + 1] for n in [k - 1, k, k + 1]) - nodes[i, j, k] * (nodes[i, j, k] - battery_charging_stations_visited[i, j, k] + 1) >= 0 for i in range(1, grid_size + 1) for j in range(1, grid_size + 1)  for k in range(1, grid_size + 1)), name='c5')


# Optimize model
m.optimize()



# Post process the results and generate a colored grid
nodes_display = np.zeros((grid_size, grid_size, grid_size), dtype=int)

for i in range(grid_size):
    for j in range(grid_size):
        for k in range(grid_size):
            if (i + 1, j + 1, k + 1) in initial_final_points:
                nodes_display[i][j][k] = 3
            elif (i + 1, j + 1, k + 1) in obstacles:
                nodes_display[i][j][k] = 4
            # elif round(battery_charging_stations_visited.X[i + 1, j + 1, k+ 1]) == 1:
            #         nodes_display[i][j][k] = 6
            elif round(nodes.X[i + 1, j + 1, k + 1]) == 1:
                nodes_display[i][j][k] = 2
            elif (i + 1, j + 1, k + 1) in battery_charging_stations:
                nodes_display[i][j][k] = 5


display_path_3d(nodes_display)
