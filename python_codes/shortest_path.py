import numpy as np
import gurobipy as gp
from gurobipy import GRB
from grid_shortest_path import display_path



# Create the required parameters
## Change input parameter values here only
grid_size = 10

np.random.seed(378) # 10, 378, 968, 1090 works # check 4, 555

obstacles_number = np.random.choice(np.arange(2 * grid_size) + 1)

battery_charging_stations_number = 2 * grid_size

points_choose = np.random.choice(np.arange(grid_size ** 2), obstacles_number + battery_charging_stations_number + 2, replace=False)

initial_final_points_choose = np.random.choice(points_choose, 2, replace=False)
initial_final_points = []

for i in initial_final_points_choose:
    initial_final_points.append(((i // grid_size) + 1, (i % grid_size) + 1))


obstacles_choose = np.random.choice(np.setdiff1d(points_choose, initial_final_points_choose), obstacles_number, replace=False)
obstacles = []

for i in obstacles_choose:
    obstacles.append(((i // grid_size) + 1, (i % grid_size) + 1))


battery_charging_stations_choose = np.setdiff1d(np.setdiff1d(points_choose, initial_final_points_choose), obstacles_choose)
battery_charging_stations = []

for i in battery_charging_stations_choose:
    battery_charging_stations.append(((i // grid_size) + 1, (i % grid_size) + 1))


battery_added = np.zeros((grid_size + 2, grid_size + 2), dtype=int)

for i in range(grid_size + 2):
    for j in range(grid_size + 2):
        if (((i, j) in battery_charging_stations) or ((i, j) in initial_final_points)):
            battery_added[i][j] = 1


distance_matrix = np.zeros((grid_size + 2, grid_size + 2, grid_size + 2, grid_size + 2))

for i in range(grid_size + 2):
    for j in range(grid_size + 2):
        for k in range(grid_size + 2):
            for l in range(grid_size + 2):
                if (k, l) == (i, j - 1) or (k, l) == (i, j + 1) or (k, l) == (i - 1, j) or (k, l) == (i + 1, j):
                    distance_matrix[i][j][k][l] = 1
                elif (k, l) == (i - 1, j - 1) or (k, l) == (i - 1, j + 1) or (k, l) == (i + 1, j - 1) or (k, l) == (i + 1, j + 1):
                    distance_matrix[i][j][k][l] = 1.4142


bool_initial_final_points = np.zeros((grid_size + 2, grid_size + 2), dtype=int)

for i in range(grid_size + 2):
    for j in range(grid_size + 2):
        if (i, j) in initial_final_points:
            bool_initial_final_points[i][j] = 1



# Create a new model
m = gp.Model('shortest_path')


# Create decision variables
nodes = m.addMVar((grid_size + 2, grid_size + 2), vtype=GRB.BINARY, name='nodes')
battery_charging_stations_visited = m.addMVar((grid_size + 2, grid_size + 2), vtype=GRB.BINARY, name='battery_charging_stations_visited')


# Set objective function
m.setObjective(gp.quicksum(distance_matrix[i][j][k][l] * nodes[i, j] * nodes[k, l] for i in range(1, grid_size + 1) for j in range(1, grid_size + 1) for k in range(1, grid_size + 1) for l in range(1, grid_size + 1)) / 2, GRB.MINIMIZE)


# Add constraints
## Constraint 1 - Initial and final points should be 1
m.addConstrs((nodes[initial_final_points[i][0], initial_final_points[i][1]] - 1 == 0 for i in range(2)), name='c0')

## Constraint 2 - Obstacles should be 0
m.addConstrs((nodes[obstacles[i][0], obstacles[i][1]] == 0 for i in range(obstacles_number)), name='c1')

## Constraint 3 - Padded points should be 0
m.addConstrs((nodes[i, j] == 0 for i in range(grid_size + 2) for j in [0, grid_size + 1]), name='c2')
m.addConstrs((nodes[i, j] == 0 for i in [0, grid_size + 1] for j in range(1, grid_size + 1)), name='c2')

## Constraint 4 - Define battery_charging_stations_visited as intersection of visited points & battery_charging_stations
m.addConstrs((battery_charging_stations_visited[i, j] - battery_added[i][j] * nodes[i, j] ==  0 for i in range(grid_size + 2) for j in range(grid_size + 2)), name='c3')

## Constraint 5 - Path should be connected
m.addConstrs((nodes[i, j] * (gp.quicksum(nodes[k, l] for k in [i - 1, i, i + 1] for l in [j - 1, j, j + 1]) + bool_initial_final_points[i][j] - 3) == 0 for i in range(1, grid_size + 1) for j in range(1, grid_size + 1)), name='c4')

## Constraint 6 - Battery level should be positive at each hop (have considered maximum possible hops as two)
m.addConstrs((gp.quicksum(battery_charging_stations_visited[k, l] for k in [i - 1, i, i + 1] for l in [j - 1, j, j + 1]) - nodes[i, j] * (nodes[i, j] - battery_charging_stations_visited[i, j] + 1) >= 0 for i in range(1, grid_size + 1) for j in range(1, grid_size + 1)), name='c5')


# Optimize model
m.optimize()



# Post process the results and generate a colored grid
nodes_display = np.zeros((grid_size, grid_size), dtype=int)

for i in range(grid_size):
    for j in range(grid_size):
        if (i + 1, j + 1) in initial_final_points:
            nodes_display[i][j] = 3
        elif (i + 1, j + 1) in obstacles:
            nodes_display[i][j] = 4
        elif round(battery_charging_stations_visited.X[i + 1, j + 1]) == 1:
                nodes_display[i][j] = 6
        elif round(nodes.X[i + 1, j + 1]) == 1:
            nodes_display[i][j] = 2
        elif (i + 1, j + 1) in battery_charging_stations:
            nodes_display[i][j] = 5


display_path(nodes_display)
