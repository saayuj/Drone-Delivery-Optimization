import numpy as np
from grid import display_path


grid_size = 10


nodes = np.zeros((grid_size, grid_size), dtype=int)

# nodes[0][0] = 6
# nodes[1][4] = 6
# nodes[1][7] = 6
# nodes[2][2] = 6
# nodes[3][9] = 6
# nodes[5][2] = 6
# nodes[6][6] = 6
# nodes[9][1] = 6
# nodes[9][7] = 6

nodes[0][0] = 6
nodes[1][6] = 6
nodes[3][9] = 6
nodes[4][3] = 6
nodes[8][0] = 6
nodes[9][8] = 6


nodes[0][2] = 5
nodes[0][5] = 5
nodes[1][0] = 5
nodes[1][1] = 5
nodes[1][3] = 5
nodes[2][9] = 5
nodes[3][8] = 5
nodes[3][6] = 5
nodes[4][0] = 5
nodes[4][8] = 5
nodes[5][0] = 5
nodes[5][1] = 5
nodes[5][3] = 5
nodes[5][7] = 5
nodes[5][8] = 5
nodes[5][9] = 5
nodes[6][3] = 5
nodes[7][0] = 5
nodes[7][3] = 5
nodes[7][5] = 5
nodes[7][6] = 5
nodes[7][9] = 5
nodes[8][1] = 5
nodes[8][2] = 5
nodes[8][3] = 5
nodes[8][4] = 5
nodes[8][7] = 5
nodes[9][4] = 5
nodes[9][5] = 5
nodes[9][9] = 5


display_path(nodes, 6969)
