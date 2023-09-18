from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint

#отрисовка ребер и вершин
class Vertex:
    def __init__(self, number, x, y, color=QColor(206,206,206)):
        self.number = number
        self.x = x
        self.y = y
        self.color = color
        self.r = 30
        
    def draw(self,pq:QPainter):
        pq.setBrush(self.color)
        pq.drawEllipse(QPoint(self.x,self.y), self.r, self.r)
        pq.drawText(self.x-5,self.y+5,str(self.number))
    #���������� �������

        

  #  def check_vert(self,x,y):
#        return (self.x - x) ** 2 + (self.y - y) ** 2 <= self.r ** 2
