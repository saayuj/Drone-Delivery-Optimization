import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def display_path(grid, time):
    '''
    0 represent as empty block - displayed as white
    2 represent path points - displayed as green 
    3 represent start end point - displayed as red
    4 represent blocked point - displayed as black
    5 represent charging station - displayed as blue color
    parameter:
        grid: 2-d numpy array - but may work with 2-d python list
    '''
    if not isinstance(grid, (np.ndarray)):
        grid = np.array(grid, dtype=np.float16)
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # make color map
    my_cmap = colors.ListedColormap(['white', 'green', 'red', 'black', 'blue', 'purple'])
    bounds = [0, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1]
    norm = colors.BoundaryNorm(bounds, my_cmap.N)
    n, m = grid.shape
    for x in range(n + 1):
        ax.axhline(x, lw=1, color='k', zorder=5)
    for x in range(m + 1):
        ax.axvline(x, lw=1, color='k', zorder=5)
    # draw the boxes
    ax.imshow(np.array(grid, dtype=np.float16), interpolation='none', cmap=my_cmap, norm=norm, extent=[0, n, 0, m], zorder=0)

    fig.savefig(f'grid{time}.png')
