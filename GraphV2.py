from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import *
from vertex import *
import math
#отрисовка графа
class Graph():
    def __init__(self,matr):
        self.matr=matr
        self.vert_list = [] # список вершин
    def add_vert(self, i, x, y):
        self.vert_list.append(Vertex(i+1,x,y,))
    def draw_graph(self, pq:QPainter,n,x=0,y=0):
        flag=[False]*n
        if x!=0:
            self.x0=x
        else:
            self.x0=200
        if y!=0:
            self.x0=y
        else:
            self.y0=600
        r=140
        for i in range(n):
            fi=(2*math.pi*i)/n
            self.add_vert(i,round(self.x0+r*math.cos(fi)),round(self.y0+r*math.sin(fi)))
        for i in range(n):
            for j in range(i,n):
                if int(self.matr[i][j])>0 and not flag[i]:
                    pq.drawLine(QPoint(self.vert_list[i].x,self.vert_list[i].y), QPoint(self.vert_list[j].x,self.vert_list[j].y))
            flag[i]=True
            self.vert_list[i].draw(pq)