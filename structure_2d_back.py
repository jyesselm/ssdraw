from PySide.QtCore import *
from PySide.QtGui import *
from rnamake import secondary_structure, secondary_structure_parser, primitives, graph


class Residue2D(secondary_structure.Residue):
    def __init__(self,  name, dot_bracket, num, chain_id, uuid, i_code=""):
        super(self.__class__, self).__init__( name, dot_bracket, num, chain_id, uuid, i_code)

        if self.name == "A":
            self.color = Qt.yellow
        elif self.name == "G":
            self.color = Qt.red
        elif self.name == "U":
            self.color = Qt.blue
        elif self.name == "C":
            self.color = Qt.green
        else:
            self.color = Qt.black

        self.x = 0
        self.y = 0
        self.go_x = 0
        self.go_y = 0

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, p):
        p.setBrush(self.color)
        center = QPoint(self.x, self.y)
        p.drawEllipse(center, 7, 7)


class GraphNode2D(object):
    pass


class Graph2D(object):
    def __init__(self):
        self.graph = graph.GraphStatic()


