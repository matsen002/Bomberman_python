from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Authors(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setGeometry(250, 250, 200, 200)
        self.setWindowTitle('Authors')
        self.initT()

    def initT(self):

        self.text = ('Autor:\n'
                     'Sendrowicz Mateusz\n')
        self.show()

# tworzenie tekstu
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):

        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('Calibri', 12))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

class About(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setGeometry(250, 250, 200, 200)
        self.setWindowTitle('About')
        self.initT()

    def initT(self):

        self.text = ('Bomberman 2017\n'
                     'Zasady chyba jasne')
        self.show()

# tworzenie tekstu
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):

        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)
