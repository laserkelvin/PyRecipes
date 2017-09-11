from matplotlib import pyplot as plt

""" General Matplotlib functions that deal with the figure/axis.
    These are either used to

"""

def remove_borders(axis, border_list=["top", "right"]):
    """ Removes borders from a Matplotlib axis.
        Arguments:

        axis - Matplotlib axis object instance.
        border_list - A list of border sides to be removed.

        Borders are specified by: top, left, right, bottom.
    """
    for border in border_list:
        axis.spines[border].set_visible(False)

def scientific_notation(axis):
    """ Forces the axis labels to be numeric, not scientific notation."""
    axis.ticklabel_format(useOffset=False)

def general_format(fig, axis):
    """ General function that will format a Matplotlib subplot to remove
        some common annoyances that figures have.
    """
    fig.tight_layout()
    scientific_notation(axis)        # Remove scientific notation
