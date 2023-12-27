import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def create_brighter_green_cmap():
    # Define the original 'brg' colormap
    original_cmap = plt.get_cmap('brg_r')

    # Extract the colormap values
    cmap_values = original_cmap(np.linspace(0, 1, 256))

    # Define the linear function for brighten_factor
    brighten_factor = np.linspace(1.5, 1, 256)

    # Apply the linear function to the green component
    cmap_values[:, 1] = np.clip(cmap_values[:, 1] * brighten_factor, 0, 1)

    # Create a new colormap
    brighter_green_cmap = ListedColormap(cmap_values)

    return brighter_green_cmap

def create_lighter_green_cmap():
    # Define the original 'brg' colormap
    original_cmap = plt.get_cmap('brg_r')

    # Extract the colormap values
    cmap_values = original_cmap(np.linspace(0, 1, 256))

    # Set the green component to a light green color
    cmap_values[:, 1] = 0.8  # You can experiment with different values for light green

    # Create a new colormap
    lighter_green_cmap = ListedColormap(cmap_values)

    return lighter_green_cmap