import numpy as np
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

def test_draw_circles():
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, aspect='equal')

    #fig.axes.get_xaxis().set_visible(False)
    #fig.axes.get_yaxis().set_visible(False)
    N = 3
    x = np.random.rand(N)
    y = np.random.rand(N)
    radii = 0.1*np.random.rand(N)
    patches = []
    for x1, y1, r in zip(x, y, radii):
        print x1, y1, r
        circle = Circle((x1, y1), r)
        patches.append(circle)

    for p in patches:
        ax.add_patch(p)

    plt.show()

def test_draw_text():
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, aspect='equal')

    ax.text(0.95, 0.01, 'colored text in axes coords',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='green', fontsize=15)


    plt.show()



test_draw_text()