import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors



def display_path_3d(grid):

    """
    0/1 represents empty points - displayed as white
    2 represents path points - displayed as green 
    3 represents start & end points - displayed as red
    4 represents blocked points/obstacles - displayed as black
    5 represents battery charging stations - displayed as blue
    6 represents visited battery charging stations - displayed as purple
    
    parameter:
        grid: 3-d numpy array - but may work with 3-d python list
    """

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Get the dimensions of the array
    x_size, y_size, z_size = grid.shape

    # Create a grid of coordinates for the 3D plot
    x, y, z = np.meshgrid(np.arange(x_size), np.arange(y_size), np.arange(z_size))

    # Flatten the array and coordinates
    array_flat = grid.flatten()
    x_flat = x.flatten()
    y_flat = y.flatten()
    z_flat = z.flatten()

    # Plot the 3D scatter plot with the custom colormap
    my_cmap = colors.ListedColormap(['white', 'green', 'red', 'black', 'blue', 'purple'])
    bounds = [0, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1]
    norm = colors.BoundaryNorm(bounds, my_cmap.N)

    sc = ax.scatter(x_flat, y_flat, z_flat, c=array_flat, cmap=my_cmap, norm=norm)

    # Add a colorbar to the plot
    # plt.colorbar(sc, ax=ax, label='Value')

    # Add labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Show the plot
    plt.show()

    # Save the figure
    fig.savefig('grid_shortest_path_3d.png')
