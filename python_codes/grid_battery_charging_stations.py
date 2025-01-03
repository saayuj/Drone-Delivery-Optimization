import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors



def display_path(grid):

    '''
    0/1 represents empty points - displayed as white
    2 represents blocked points/obstacles - displayed as black
    3 represents battery charging stations - displayed as blue
    
    parameter:
        grid: 2-d numpy array - but may work with 2-d python list
    '''

    if not isinstance(grid, (np.ndarray)):
        grid = np.array(grid, dtype=np.float16)
    
    fig, ax = plt.subplots(1, 1, tight_layout=True)

    # Make color map
    my_cmap = colors.ListedColormap(['white', 'black', 'blue', 'green', 'red', 'purple'])
    bounds = [0, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1]
    norm = colors.BoundaryNorm(bounds, my_cmap.N)
    n, m = grid.shape

    for x in range(n + 1):
        ax.axhline(x, lw=1, color='k', zorder=5)
    
    for x in range(m + 1):
        ax.axvline(x, lw=1, color='k', zorder=5)
    
    # Draw the boxes
    ax.imshow(np.array(grid, dtype=np.float16), interpolation='none', cmap=my_cmap, norm=norm, extent=[0, n, 0, m], zorder=0)

    fig.savefig('grid_battery_charging_stations.png')
    