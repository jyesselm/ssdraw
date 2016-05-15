from PySide.QtCore import *
from PySide.QtGui import *
from rnamake import secondary_structure_parser, secondary_structure


class DrawCircles(QWidget):
    def __init__(self, seq, ss, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(700, 700, 750, 750)
        self.setWindowTitle('Draw circles')

        p = secondary_structure_parser.SecondaryStructureParser()
        self.mg = p.parse_to_motif_graph(seq, ss)

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        # for circle make the ellipse radii match
        radx = 10
        rady = 10
        # draw red circles
        paint.setPen(Qt.black)
        for k in range(125, 700, 20):
            center = QPoint(k, k)
            # optionally fill each circle yellow
            paint.setBrush(Qt.green)
            paint.drawEllipse(center, radx, rady)
        paint.end()

    def paint_bp(self, n):
        pass




app = QApplication([])
circles = DrawCircles("GGACC", "((.))")
circles.show()
app.exec_()