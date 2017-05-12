from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import it
import map
import sys
from xml.dom import minidom
import menu

class Bomberman(QMainWindow):

    def __init__(self):
        super(Bomberman, self).__init__()

        self.glcpdx = 0 #globalny licznik czasu potrzebny do xmla
        self.zkmbz = [] #zmiany ktore maja byc zachowane
                        # w postaci kiedy, gdzie, co, czyli kolejne wierze

        self.speed = 10
        self.mapa = map.Map()
        self.agenty = []
        self.licznik = 0
        self.writeToXML_vec = []

        #"generowanie" botow
        self.agenty.append(it.It(1,1,1))
        self.agenty.append(it.It(1,38,2))
        self.agenty.append(it.It(20,1,2))
        self.agenty.append(it.It(20,38,1))
        self.agenty.append(it.It(38,1,3))
        self.agenty.append(it.It(38,38,1))

        self.timer = QBasicTimer()
        self.bomba = it.Bomb(self)

        for i in range(1,6):
            self.set_map_fun(self.agenty[i].get_x(),self.agenty[i].get_y(),-1)
        self.set_map_fun(self.agenty[0].get_x(), self.agenty[0].get_y(), -2)

        self.margin = 0

        self.box = map.drawMap(self.height(), self.width(), self, self.margin, self.mapa.get_all())

        self.initUi()

    def initUi(self):
        # Start
        startAction = QAction(QIcon('exit.png'), '&Start', self)
        startAction.triggered.connect(self.start)
        # Stop
        stopAction = QAction(QIcon('exit.png'), '&Stop', self)
        stopAction.triggered.connect(self.stop)
        # Wczytaj
        readAction = QAction(QIcon('exit.png'), '&Wczytaj', self)
        readAction.triggered.connect(self.read)
        # Exit
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setStatusTip('Exit application')  # zamykanie
        exitAction.triggered.connect(self.zamknij)
        # About
        helpAction = QAction(QIcon('exit.png'), '&About', self)
        helpAction.triggered.connect(self.about)  # wywolanie kolejnego okna
        # Authors
        authorsAction = QAction(QIcon('exit.png'), '&Authors', self)
        authorsAction.triggered.connect(self.authors)
        self.ab = None
        self.au = None
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')  # umieszczenie w menu "File"
        fileMenu.addAction(startAction)
        fileMenu.addAction(stopAction)
        fileMenu.addAction(readAction)
        fileMenu.addAction(exitAction)
        fileMenu2 = menubar.addMenu('&Help')
        fileMenu2.addAction(helpAction)  # umiezczenie w menu "About"
        fileMenu2.addAction(authorsAction)  # umiezczenie w menu "Authors"

        self.setGeometry(250, 250, 550, 550)
        self.resize(600, 630)
        self.setWindowTitle('Bomberman')

        self.show()

    def about(self):
        self.ab = menu.About()
        self.ab.show()

    def authors(self):
        self.au = menu.Authors()
        self.au.show()

    def zamknij(self):
        sys.exit()

    def start(self):
        self.timer.start(self.speed, self)

    def stop(self):
        self.timer.stop()
        self.writeToXML()

    def read(self):
        self.readFromXml()

    def set_map_fun(self, x, y, val):
        self.mapa.set_map(x, y, val)
        self.zkmbz.append([self.glcpdx, x, y, val])

    def ruch(self, i):
        x = self.agenty[i].get_x()
        y = self.agenty[i].get_y()
        move = self.agenty[i].get_move()

        ruszyl = False

        if i == 0:
            a_col = -2
        else:
            a_col = -1
        if move == 1:  # w dol
            if self.mapa.get_map(x + 1, y) == 0:
                self.set_map_fun(x, y, 0)
                self.set_map_fun(x + 1, y, a_col)
                self.agenty[i].set_x(x + 1)
                ruszyl = True
            elif self.mapa.get_map(x - 1, y) == 0:
                self.agenty[i].set_move(2)
        elif move == 2:  # w gore
            if self.mapa.get_map(x - 1, y) == 0:
                self.set_map_fun(x, y, 0)
                self.set_map_fun(x - 1, y, a_col)
                self.agenty[i].set_x(x - 1)
                ruszyl = True
            elif self.mapa.get_map(x + 1, y) == 0:
                self.agenty[i].set_move(1)
        elif move == 3:  # w prawo
            if self.mapa.get_map(x, y + 1) == 0:
                self.set_map_fun(x, y, 0)
                self.set_map_fun(x, y + 1, a_col)
                self.agenty[i].set_y(y + 1)
                ruszyl = True
            elif self.mapa.get_map(x, y - 1) == 0:
                self.agenty[i].set_move(4)
        elif move == 4:  # w lewo
            if self.mapa.get_map(x, y - 1) == 0:
                self.set_map_fun(x, y, 0)
                self.set_map_fun(x, y - 1, a_col)
                self.agenty[i].set_y(y - 1)
                ruszyl = True
            elif self.mapa.get_map(x, y + 1) == 0:
                self.agenty[i].set_move(3)

        if self.bomba.new_bomb and i == 0 and ruszyl == True:      #odswiezamy bombe tylko gdy ruszy sie ten co ja postawil
            self.set_map_fun(self.bomba.get_x(-1), self.bomba.get_y(-1), 3)
            self.bomba.new_bomb = False
            self.repaint()

    def bomb_boom(self):    #glowna funkcja od wybuchow
        x = self.bomba.get_x(0)
        y = self.bomba.get_y(0)
        for k in range(4):
            for i in range(self.bomba.get_type(0) + 1):
                x_vec = [x + i, x - i, x, x]
                y_vec = [y, y, y + i, y - i]
                val = self.mapa.get_map(x_vec[k], y_vec[k])
                if val == 1:
                    break
                elif val == 2:
                    self.set_map_fun(x_vec[k], y_vec[k], 0)
                elif val == -1:
                    for j in range(len(self.agenty)):
                        if self.agenty[j].get_x() == x_vec[k] and self.agenty[j].get_y() == y_vec[k]:
                            if j != len(self.agenty) - 1:
                                new_agenty = self.agenty[:j] + self.agenty[j + 1:]
                            else:
                                new_agenty = self.agenty[:j]
                            self.agenty = new_agenty
                            self.set_map_fun(x_vec[k], y_vec[k], 0)
                            break
                elif val == -2:
                    print('koniec gry')

    def writeToXML(self):
        doc = minidom.Document()

        root = doc.createElement("Game")

        doc.appendChild(root)

        mapa = doc.createElement('Mapa')

        for j in range(40):
            wiersz = doc.createElement('Wiersz')
            mapa.appendChild(wiersz)
            for i in range(40):
                kolumna = doc.createElement('Kolumna')

                wart = doc.createTextNode(str(self.mapa.get_map(j, i)))
                kolumna.appendChild(wart)
                wiersz.appendChild(kolumna)

        root.appendChild(mapa)

        rozgrywka = doc.createElement('Rozgrywka')

        for i in range(len(self.zkmbz)):
            kolumna = doc.createElement(str(self.zkmbz[i][0]))
            rozgrywka.appendChild(kolumna)
            for j in range(1,4):
                wiersz = doc.createElement(str(self.zkmbz[i][j]))
                kolumna.appendChild(wiersz)

        root.appendChild(rozgrywka)

        doc.writexml(open('data1.xml', 'w'),
                     indent="  ",
                     addindent="  ",
                     newl='\n')

        doc.unlink()

    def readFromXml(self):
        dom = minidom.parse("data.xml")
        a = 0
        print(a)
        #name = doc.getElementsByTagName("Game")[0]
        #print(name.firstChild.data)
    '''
        staffs = doc.getElementsByTagName("staff")
        for staff in staffs:
            sid = staff.getAttribute("id")
            nickname = staff.getElementsByTagName("nickname")[0]
            salary = staff.getElementsByTagName("salary")[0]
            print("id:%s, nickname:%s, salary:%s" %
                  (sid, nickname.firstChild.data, salary.firstChild.data))
    '''
    def timerEvent(self, event):

        if self.bomba.bedzie_boom > 0:
            czy_bylo_booom = False
            if event.timerId() == self.bomba.bombs_timer_tab[0].timerId():
                self.set_map_fun(self.bomba.get_x(0), self.bomba.get_y(0), 0)
                self.bomb_boom()
                self.bomba.bedzie_boom -= 1
                self.bomba.bomb_boom()     #usuwanie informacji o bombie

        if event.timerId() == self.timer.timerId():
            self.licznik += 1
            if self.licznik == 50:
                self.licznik = 0
                #print('x: ', self.agenty.get_x(0), ' y: ', self.agenty.get_y(0))
                for i in range(1, len(self.agenty)):
                    self.ruch(i)
                self.glcpdx += 1
                    #print('x: ', self.agenty.get_x(i), ' y: ', self.agenty.get_y(i))
                #print('')
            self.repaint()
        else:
            super(Bomberman, self).timerEvent(event)

    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_Left:
            self.agenty[0].set_move(4)
            self.ruch(0)
        elif key == Qt.Key_Right:
            self.agenty[0].set_move(3)
            self.ruch(0)
        elif key == Qt.Key_Down:
            self.agenty[0].set_move(1)
            self.ruch(0)
        elif key == Qt.Key_Up:
            self.agenty[0].set_move(2)
            self.ruch(0)
        elif key == Qt.Key_Space:
            x_b = self.agenty[0].get_x()
            y_b = self.agenty[0].get_y()
            self.bomba.add_bomb(x_b, y_b, 3)
            self.set_map_fun(x_b, y_b, 3)
            self.bomba.bedzie_boom += 1
            self.bomba.new_bomb = True
        elif key == Qt.Key_Escape:
            sys.exit()

        else:
            super(Bomberman, self).keyPressEvent(event)

    def paintEvent(self, event):
        self.box.draw()

def main():
    app = QApplication(sys.argv)
    bomberman = Bomberman()
    sys.exit(app.exec_())

#if __name__ == '__main__':
main()