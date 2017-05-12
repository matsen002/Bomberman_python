from PyQt5 import QtGui, QtCore

class It:

    def __init__(self, x , y, move):
        self.x = x
        self.y = y
        self.move = move

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def set_move(self, m):
        self.move = m

    def get_move(self):
        return self.move

class Bomb:

    def __init__(self, q_window):
        self.q_window = q_window

        self.x = []
        self.y = []
        self.type = []
        self.time_to_boooom = 5
        self.new_bomb = False
        self.bomb_speed = 4000

        self.bombs_timer_tab = []
        self.bedzie_boom = 0

    def add_bomb(self, x, y, type):
        self.type.append(type)
        self.y.append(y)
        self.x.append(x)
        self.b_timer()

    def b_timer(self):
        new_timer = QtCore.QBasicTimer()
        new_timer.start(self.bomb_speed, self.q_window)
        self.bombs_timer_tab.append(new_timer)

    def get_x(self, i):
        return self.x[i]

    def get_y(self, i):
        return self.y[i]

    def get_type(self, i):
        return self.type[i]

    def bomb_boom(self):
        #usuwanie informacji o bombie
        self.x = self.x[1:]
        self.y = self.y[1:]
        self.type = self.type[1:]

        self.bombs_timer_tab = self.bombs_timer_tab[1:]