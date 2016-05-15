import random
import math

from PySide.QtCore import *
from PySide.QtGui import *
from rnamake import secondary_structure, secondary_structure_parser

import structure_2d


NODE_R = 6
PRIMARY_SPACE = 20
PAIR_SPACE = 23
CELL_PADDING = 40

class ChainContainers(object):
    def __init__(self, c, m, space):
        self.c = c
        self.m = m
        self.space = space


class TestDrawResidues(QWidget):
    def __init__(self, seq, ss, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(700, 700, 750, 750)
        self.setWindowTitle('Test Draw Residues')
        s = secondary_structure.Structure(sequence=seq, dot_bracket=ss,
                                          rtype=structure_2d.Residue2D)
        res = s.residues()

        x = 100
        y = 100
        cross_x = -1
        cross_y = 0
        go_x = 0
        go_y = 1

        npairs = 0
        length_walker = PAIR_SPACE / 2.0
        circle_length = (len(res)+1) * PRIMARY_SPACE + (npairs + 1) * PAIR_SPACE
        circle_radius = circle_length / (2 * math.pi)

        for i ,r in enumerate(res):

            length_walker += PRIMARY_SPACE
            rad_angle = length_walker / circle_length * 2 * math.pi - math.pi / 2.0
            print length_walker, rad_angle
            r.x = 100 + math.cos(rad_angle) * cross_x * circle_radius + \
                  math.sin(rad_angle) * go_x * circle_radius

            r.y = 100 + math.cos(rad_angle) * cross_y * circle_radius + \
                  math.sin(rad_angle) * go_y * circle_radius


        self.res = res


    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        paint.setPen(Qt.black)

        for r in self.res:
            r.draw(paint)

        paint.end()


class TestDrawBasepairs(QWidget):
    def __init__(self, seq, ss, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(700, 700, 750, 750)
        self.setWindowTitle('Test Draw Basepairs')
        s = secondary_structure.Structure(sequence=seq, dot_bracket=ss,
                                          rtype=structure_2d.Residue2D)
        p = secondary_structure_parser.SecondaryStructureParser()
        m = p.parse_to_motif(structure=s)

        x = 300
        y = 100
        cross_x = -1
        cross_y = 0
        go_x = 0
        go_y = 1

        seen = {}
        for i, r in enumerate(m.residues()):
            bp = m.get_basepair(res1=r)
            if bp is not None:
                if bp in seen:
                    continue
                seen[bp] = 1

            r.set_pos(x, y)
            r.go_x = go_x
            r.go_y = go_y

            if bp is not None:
                o_res = bp.partner(r)
                cross_x = r.go_y
                cross_y = r.go_x
                new_x = x + cross_x * PAIR_SPACE
                new_y = y - cross_y * PAIR_SPACE
                o_res.set_pos(new_x, new_y)

            x += go_x * PRIMARY_SPACE
            y += go_y * PRIMARY_SPACE

        self.res = m.residues()

        print m

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        paint.setPen(Qt.black)

        for r in self.res:
            r.draw(paint)

        paint.end()


class TestDrawMotifs(QWidget):
    def __init__(self, seq, ss, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(700, 700, 750, 750)
        self.setWindowTitle('Test Draw Motifs')
        s = secondary_structure.Structure(sequence=seq, dot_bracket=ss,
                                          rtype=structure_2d.Residue2D)
        p = secondary_structure_parser.SecondaryStructureParser()
        ssg = p.parse(structure=s)
        motifs = p.parse_to_motifs(structure=s)
        for n in ssg.graph:
            print n.data.residues

        print len(motifs)

        exit()

        x = 300
        y = 100
        cross_x = -1
        cross_y = 0
        go_x = 0
        go_y = 1

        seen = {}
        for i, r in enumerate(m.residues()):
            bp = m.get_basepair(res1=r)
            if bp is not None:
                if bp in seen:
                    continue
                seen[bp] = 1

            r.set_pos(x, y)
            r.go_x = go_x
            r.go_y = go_y

            if bp is not None:
                o_res = bp.partner(r)
                cross_x = r.go_y
                cross_y = r.go_x
                new_x = x + cross_x * PAIR_SPACE
                new_y = y - cross_y * PAIR_SPACE
                o_res.set_pos(new_x, new_y)

            x += go_x * PRIMARY_SPACE
            y += go_y * PRIMARY_SPACE

        self.res = m.residues()

        print m

    def set_coords_for_chain(self, c):
        pass

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        paint.setPen(Qt.black)

        for r in self.res:
            r.draw(paint)

        paint.end()



def test_draw_res():
    app = QApplication([])
    c = TestDrawResidues("GGGGGGGGG", ".........")
    c.show()
    app.exec_()

def test_draw_basepairs():
    app = QApplication([])
    c = TestDrawBasepairs("GGGAGACCCC", "(((.(.))))")
    c.show()
    app.exec_()

def test_draw_motifs():
    app = QApplication([])
    c = TestDrawMotifs("GGGAAGACCCC", "(((..(.))))")
    c.show()
    app.exec_()



test_draw_motifs()
