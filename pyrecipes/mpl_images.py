from matplotlib import pyplot as plt

def add_image_overlay(axis, filepath, zoom=0.15, position=[0., 0.]):
    """ Function to add an image to a Matplotlib axis.

        Arguments:

        axis - A Matplotlib `axis` object instance.
        filepath - Path to the target image file.
        zoom - Float that determines the scale of the image.
        position - 2-tuple that sets the xy position of the image.

        Adds the image to the axis, and returns the AnnotationBbox object
    """
    image = OffsetImage(plt.imread(filepath), zoom=zoom)
    image.image.axes = axis

    box = AnnotationBbox(image, position,
                        xybox=position,
                        xycoords='data',
                        frameon=False
                        )
    axis.add_artist(box)

    return box
