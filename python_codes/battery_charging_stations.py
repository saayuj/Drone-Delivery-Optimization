import numpy as np
import gurobipy as gp
from gurobipy import GRB
from grid_battery_charging_stations import display_path
from dijkstra_distance_matrix import DistanceBetweenNodes



# Create the required parameters
## Change input parameter values here only
grid_size = 10

distance_covered_by_battery_charging_station = 2 * np.sqrt(2)

np.random.seed(7) # 4, 7, 10, 378, 779, 968, 1090

obstacles_number = np.random.choice(np.arange(2 * grid_size) + 1)

obstacles_choose = np.random.choice(np.arange(grid_size ** 2), obstacles_number, replace=False)
obstacles = []
obstacles_padded = []

for i in obstacles_choose:
    obstacles.append((i // grid_size, i % grid_size))


for i in obstacles_choose:
    obstacles_padded.append(((i // grid_size) + 1, (i % grid_size) + 1))

for i in range(grid_size):
    for j in [0, grid_size + 1]:
        obstacles_padded.append((i, j))

for i in [0, grid_size + 1]:
    for j in range(1, grid_size + 1):
        obstacles_padded.append((i, j))


initial_battery_charging_station_choose = np.random.choice(np.setdiff1d(np.array([22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 36, 37, 42, 43, 44, 45, 46, 47, 52, 53, 54, 55, 56, 57, 62, 63, 64, 65, 66, 67, 72, 73, 74, 75, 76, 77]), obstacles_choose), 1)
initial_battery_charging_station = []

initial_battery_charging_station.append(initial_battery_charging_station_choose[0] // grid_size)
initial_battery_charging_station.append(initial_battery_charging_station_choose[0] % grid_size)


# Create graph, add edges and make distance matrix
node_graph = DistanceBetweenNodes()

for i in range(1, grid_size + 1):
    for j in range(1, grid_size + 1):
        for k in range(i - 1, i + 2):
            for l in range(j - 1, j + 2):
                if (i, j) in obstacles_padded or (k, l) in obstacles_padded:
                    node_graph.add_edge((i, j), (k, l), float('inf'))
                else:
                    node_graph.add_edge((i, j), (k, l), np.sqrt((i - k) ** 2 + (j - l) ** 2))


dijkstra_distance_matrix = np.zeros((grid_size, grid_size, grid_size, grid_size))

for i in range(grid_size):
    for j in range(grid_size):
        for k in range(grid_size):
            for l in range(grid_size):
                dijkstra_distance_matrix[i][j][k][l] = node_graph.dijkstra_distance((i + 1, j + 1), (k + 1, l + 1))



# Create a new model
m = gp.Model('battery_charging_stations')


# Create decision variables
battery_charging_stations = m.addMVar((grid_size, grid_size), vtype=GRB.BINARY, name='battery_charging_stations')
multiply_battery_charging_stations = m.addMVar((grid_size, grid_size, grid_size, grid_size), vtype=GRB.BINARY, name='multiply_battery_charging_stations')
edges_battery_charging_stations = m.addMVar((grid_size, grid_size, grid_size, grid_size), vtype=GRB.BINARY, name='edges_battery_charging_stations')
multiply_edges = m.addMVar((grid_size, grid_size, grid_size, grid_size), vtype=GRB.BINARY, name='multiply_edges')
visiting_time = m.addMVar((grid_size, grid_size), lb=1, ub=20, vtype=GRB.CONTINUOUS, name='visiting_time')


# Set objective function
m.setObjective(gp.quicksum(battery_charging_stations[i, j] for i in range(grid_size) for j in range(grid_size)), GRB.MINIMIZE)


# Add constraints
## Constraint 1 - No battery charging stations can be placed on obstacles
m.addConstrs((battery_charging_stations[i, j] == 0 for i, j in obstacles), name='c0')

## Constraint 2 - Define area covered by a battery charging station
m.addConstrs((gp.quicksum(battery_charging_stations[k, l] for k in range(grid_size) for l in range(grid_size) if dijkstra_distance_matrix[i][j][k][l] <= distance_covered_by_battery_charging_station) - 1 >= 0 for i in range(grid_size) for j in range(grid_size) if (i, j) not in obstacles), name='c1')

## Constraint 3 - Define multiply_battery_charging_stations to be used in the next constraint
m.addConstrs((multiply_battery_charging_stations[i, j, k, l] - battery_charging_stations[i, j] * battery_charging_stations[k, l] == 0 for i in range(grid_size) for j in range(grid_size) for k in range(grid_size) for l in range(grid_size)), name='c2')

## Constraint 4 - Define multiply_edges to be used in the next constraint
m.addConstrs((multiply_edges[i, j, k, l] - edges_battery_charging_stations[i, j, k, l] * edges_battery_charging_stations[k, l, i, j] == 0 for i in range(grid_size) for j in range(grid_size) for k in range(grid_size) for l in range(grid_size)), name='c3')

## Constraint 5 - Define edges between battery charging stations to be 1 if the distance between them is less than the permissible distance
m.addConstrs((multiply_battery_charging_stations[i, j, k, l] * (edges_battery_charging_stations[i, j, k, l] + edges_battery_charging_stations[k, l, i, j] - 2 * multiply_edges[i, j, k, l] - 1) == 0 for i in range(grid_size) for j in range(grid_size) for k in range(grid_size) for l in range(grid_size) if dijkstra_distance_matrix[i][j][k][l] <= distance_covered_by_battery_charging_station if (k, l) != (i, j)), name='c4')

## Constraint 6 - Define edges from battery charging stations to other far away, to non-battery charging stations to anywhere, from node to itself to be 0
m.addConstrs((multiply_battery_charging_stations[i, j, k, l] * edges_battery_charging_stations[i, j, k, l] == 0 for i in range(grid_size) for j in range(grid_size) for k in range(grid_size) for l in range(grid_size) if dijkstra_distance_matrix[i][j][k][l] > distance_covered_by_battery_charging_station), name='c5')
m.addConstrs((edges_battery_charging_stations[i, j, k, l] == 0 for i in range(grid_size) for j in range(grid_size) for k in range(grid_size) for l in range(grid_size) if (k, l) == (i, j)), name='c5')
m.addConstrs(((1 - multiply_battery_charging_stations[i, j, k, l]) * edges_battery_charging_stations[i, j, k, l] == 0 for i in range(grid_size) for j in range(grid_size) for k in range(grid_size) for l in range(grid_size)), name='c5')

## Constraint 7 - Only one outflow edge for each battery charging station
m.addConstrs((battery_charging_stations[i, j] * (gp.quicksum(edges_battery_charging_stations[i, j, k, l] for k in range(grid_size) for l in range(grid_size)) - 1) == 0 for i in range(grid_size) for j in range(grid_size)), name='c6')

## Constraint 8 - Only one inflow edge for each battery charging station
m.addConstrs((battery_charging_stations[k, l] * (gp.quicksum(edges_battery_charging_stations[i, j, k, l] for i in range(grid_size) for j in range(grid_size)) - 1) == 0 for k in range(grid_size) for l in range(grid_size)), name='c7')

## Constraint 9 - Set one battery charging station as depot for MTZ implementation
m.addConstr(battery_charging_stations[initial_battery_charging_station[0], initial_battery_charging_station[1]] - 1 == 0, name='c8')

## Constraint 10 - Implement MTZ subtour elimination by using visiting_time variables
m.addConstrs((visiting_time[k, l] - visiting_time[i, j] - 1 + 100 * (1 - edges_battery_charging_stations[i, j, k, l]) >= 0 for i in range(grid_size) for j in range(grid_size) for k in range(grid_size) for l in range(grid_size) if (i, j) != (initial_battery_charging_station[0], initial_battery_charging_station[1]) if (k, l) != (initial_battery_charging_station[0], initial_battery_charging_station[1])), name='c9')


# Optimize model
m.optimize()



# Post process the results and generate a colored grid
nodes_display = np.zeros((grid_size, grid_size), dtype=int)

for i in range(grid_size):
    for j in range(grid_size):
        if (i, j) in obstacles:
            nodes_display[i][j] = 2
        elif round(battery_charging_stations.X[i, j]) == 1:
            nodes_display[i][j] = 3


display_path(nodes_display)
