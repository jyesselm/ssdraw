import sys
sys.path.append("..")

import components

def test_figure():
    fig = components.Figure()
    fig.show()

def test_circle():
    fig = components.Figure()
    c = components.get_circle(0.5, 0.5, radius=0.05)
    fig.add_component(c)

    c = components.get_circle(0.2, 0.2, radius=0.05, facecolor='red')
    fig.add_component(c)

    c = components.get_circle(0.5, 0.2, radius=0.05, facecolor='green', edgewidth=5.0)
    fig.add_component(c)

    c = components.get_circle(0.9, 0.9, radius=0.05, facecolor=None, edgewidth=5.0)
    fig.add_component(c)
    fig.show()


test_circle()
