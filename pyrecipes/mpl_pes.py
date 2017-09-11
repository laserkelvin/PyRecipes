from matplotlib import pyplot as plt
import numpy as np

def make_pes(x, energies, width=5):
    """ Function to create a smooth PES, where stationary
        points are connected.

        Basically makes a linearly spaced x array which
        pads x-axis density to create the horizontal line
        for the stationary points

        Optional arguments are how many x-points to
        pad with on either side.

        The return values can be plotted with Matplotlib
        without changing anything.
    """
    new_x = np.array([])
    new_energies = list()
    for xvalue, energy in zip(x, energies):
        new_x = np.append(new_x, np.linspace(xvalue - (width * 0.05), xvalue + (width * 0.05), width * 2))
        new_energies.append([energy] * width * 2)

    return new_x, np.array(new_energies).flatten()
