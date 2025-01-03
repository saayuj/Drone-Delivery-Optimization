import imageio
import itertools
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from grid_optimal_scheduling import display_path



# Create the required parameters
## Change input parameter values here only
grid_size = 10

time = 20

number_of_drones = 2

np.random.seed(19)

number_of_delivery_location = np.random.choice([2, 3])

points_choose = np.random.choice(np.arange(grid_size ** 2), number_of_drones + number_of_delivery_location, replace=False)

warehouse_location_choose = np.random.choice(points_choose, number_of_drones, replace=False)
warehouse_location = []

for i in warehouse_location_choose:
    warehouse_location.append(((i // grid_size) + 1, (i % grid_size) + 1))


delivery_location_choose = np.setdiff1d(points_choose, warehouse_location_choose)
delivery_location = []

for i in delivery_location_choose:
    delivery_location.append(((i // grid_size) + 1, (i % grid_size) + 1))


delivery_demand = np.random.randint(1, 4, size=number_of_delivery_location)


##### Substitute values here for trial 1 #####
time = 11
number_of_delivery_location = 3
warehouse_location = [(3, 4), (7, 7)]
delivery_location = [(3, 1), (5, 6), (6, 8)]
delivery_demand = np.array([1, 2, 1])
##############################################


##### Substitute values here for trial 2 #####
time = 15
number_of_delivery_location = 2
warehouse_location = [(10, 1), (10, 10)]
delivery_location = [(3, 1), (7, 7)]
delivery_demand = np.array([1, 2])
##############################################


##### Substitute values here for trial 3 #####
time = 15
number_of_drones = 3
number_of_delivery_location = 2
warehouse_location = [(10, 1), (10, 10), (2, 8)]
delivery_location = [(3, 1), (7, 7)]
delivery_demand = np.array([1, 3])
##############################################


net_demand = np.sum(delivery_demand)

distance_matrix = np.zeros((grid_size + 2, grid_size + 2, grid_size + 2, grid_size + 2))

for i in range(grid_size + 2):
    for j in range(grid_size + 2):
        for k in range(grid_size + 2):
            for l in range(grid_size + 2):
                if (k, l) == (i, j - 1) or (k, l) == (i, j + 1) or (k, l) == (i - 1, j) or (k, l) == (i + 1, j):
                    distance_matrix[i][j][k][l] = 1
                elif (k, l) == (i - 1, j - 1) or (k, l) == (i - 1, j + 1) or (k, l) == (i + 1, j - 1) or (k, l) == (i + 1, j + 1):
                    distance_matrix[i][j][k][l] = 1.4142


combination_of_drones = list(itertools.combinations(np.arange(number_of_drones), 2))



# Create a new model
m = gp.Model('optimal_scheduling')


# Create decision variables
nodes = m.addMVar((number_of_drones, grid_size + 2, grid_size + 2, time), vtype=GRB.BINARY, name='nodes')
flag = m.addMVar((number_of_drones, time), vtype=GRB.BINARY, name='flag')
flag_temp = m.addMVar((number_of_drones, time - 1), vtype=GRB.BINARY, name='flag_temp')
flag_time = m.addMVar((number_of_drones, time - 1), vtype=GRB.INTEGER, name='flag_time') #### do not bound as integer, use min formulation to solve faster
time_taken_to_deliver = m.addMVar(number_of_drones, vtype=GRB.INTEGER, name='time_taken_to_deliver')


# Set objective function
m.setObjective(0.7 * gp.quicksum(distance_matrix[i][j][k][l] * nodes[n, i, j, t] * nodes[n, k, l, t + 1] for i in range(1, grid_size + 1) for j in range(1, grid_size + 1) for k in range(1, grid_size + 1) for l in range(1, grid_size + 1) for n in range(number_of_drones) for t in range(time - 1)) + 0.3 * gp.quicksum(time_taken_to_deliver[n] for n in range(number_of_drones)), GRB.MINIMIZE)


# Add constraints
## Constraint 1 - Warehouses (initial points) should be 1
m.addConstrs((nodes[n, warehouse_location[n][0], warehouse_location[n][1], 0] - 1 == 0 for n in range(number_of_drones)), name='c0')

## Constraint 2 - Padded points should be 0
m.addConstrs((nodes[n, i, j, t] == 0 for n in range(number_of_drones) for i in range(grid_size + 2) for j in [0, grid_size + 1] for t in range(time)), name='c1')
m.addConstrs((nodes[n, i, j, t] == 0 for n in range(number_of_drones) for i in [0, grid_size + 1] for j in range(1, grid_size + 1) for t in range(time)), name='c1')

## Constraint 3 - Path should be connected
m.addConstrs((gp.quicksum(nodes[n, k, l, t + 1] for k in [i - 1, i, i + 1] for l in [j - 1, j, j + 1]) - nodes[n, i, j, t] >= 0 for n in range(number_of_drones) for i in range(1, grid_size + 1) for j in range(1, grid_size + 1) for t in range(time - 1)), name='c2')

## Constraint 4 - Only one node should be 1 at a particular time
m.addConstrs((gp.quicksum(nodes[n, i, j, t] for i in range(1, grid_size + 1) for j in range(1, grid_size + 1)) - 1 == 0 for n in range(number_of_drones) for t in range(time)), name='c3')

## Constraint 5 - Flag initialized to 0
m.addConstrs((flag[n, 0] == 0 for n in range(number_of_drones)), name='c4')

## Constraint 6 - Flag operation for delivery (0)
m.addConstrs(((1 - flag[n, t]) * (flag[n, t + 1] - gp.quicksum(nodes[n, delivery_location[i][0], delivery_location[i][1], t + 1] for i in range(number_of_delivery_location))) == 0 for n in range(number_of_drones) for t in range(time - 1)), name='c5')

## Constraint 7 - Flag operation for returning to warehouse (1)
m.addConstrs((flag[n, t] * (flag[n, t + 1] + nodes[n, warehouse_location[n][0], warehouse_location[n][1], t + 1] - 1) == 0 for n in range(number_of_drones) for t in range(time - 1)), name='c6')

## Constraint 8 - Defining flag_temp in terms of flag to be used in the next two constraints
m.addConstrs((flag_temp[n, t - 1] - flag[n, t] * flag[n, t - 1] == 0 for n in range(number_of_drones) for t in range(1, time)), name='c7')

## Constraint 9 - Supply satisfaction for warehouse
m.addConstr(gp.quicksum(nodes[n, warehouse_location[i][0], warehouse_location[i][1], t] * (flag[n, t - 1] - flag_temp[n, t - 1]) for n in range(number_of_drones) for t in range(1, time) for i in range(number_of_drones)) - net_demand == 0, name='c8')

## Constraint 10 - Demand satisfaction for delivery locations
m.addConstrs((gp.quicksum(nodes[n, delivery_location[i][0], delivery_location[i][1], t] * (flag[n, t] - flag_temp[n, t - 1]) for n in range(number_of_drones) for t in range(1, time)) - delivery_demand[i] == 0 for i in range(number_of_delivery_location)), name='c9')

## Constraint 11 - Collision avoidance for drones
m.addConstrs((nodes[i, k, l, t] * nodes[j, k, l, t] == 0 for i, j in combination_of_drones for k in range(1, grid_size + 1) for l in range(1, grid_size + 1) for t in range(time)), name='c10')

## Constraint 12 - Defining flag_time in terms of time and flag to be used in the next constraint
m.addConstrs((flag_time[n, t - 1] - t * flag[n, t - 1] * (1 - flag[n, t]) == 0 for n in range(number_of_drones) for t in range(1, time)), name='c11')

## Constraint 13 - Defining the time_taken_to_deliver by each drone to be used in the objective function
for n in range(number_of_drones):
    maxVarsList = [flag_time[n, t] for t in range(time - 1)]

    m.addGenConstrMax(time_taken_to_deliver[n], maxVarsList, name='c12')


# Optimize model
m.optimize()



# Post processing the results and generating colored grids and a GIF
frames = []

for i in range(time):
    nodes_display = np.zeros((grid_size, grid_size), dtype=int)

    for k in range(grid_size):
        for l in range(grid_size):
            if (k + 1, l + 1) in warehouse_location:
                nodes_display[k][l] = 2
            elif (k + 1, l + 1) in delivery_location:
                nodes_display[k][l] = 3

            for j in range(number_of_drones):
                if round(nodes.X[j, k + 1, l + 1, i]) == 1:
                    nodes_display[k][l] = j + 4


    display_path(nodes_display, i)

    image  = imageio.v2.imread(f'grid_optimal_scheduling{i}.png')
    frames.append(image)


imageio.mimsave('grid_optimal_scheduling.gif', frames, fps=1)
