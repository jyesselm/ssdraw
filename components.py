import matplotlib.pyplot as plt
from matplotlib.patches import Circle


class Figure(object):
    def __init__(self, size=(10,10)):
        self.fig = plt.figure(figsize=size)
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        #self.ax.axis("off")

    def add_component(self, c):
        self.ax.add_patch(c)

    def add_text(self, x, y, text, fontsize=12):
        self.ax.text(x, y, text, fontsize=fontsize,
                     verticalalignment='center', horizontalalignment='center')

    def show(self):
        plt.show()

    def save(self):
        pass


def get_circle(x, y, radius=0.01, facecolor='blue', edgecolor='black',
               edgewidth=None, edgestyle='solid'):

    if facecolor is None:
        fill = False
    else:
        fill = True

    return Circle((x, y), radius=radius, facecolor=facecolor,
                  fill=fill, edgecolor=edgecolor, linewidth=edgewidth,
                  linestyle=edgestyle)