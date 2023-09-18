import sys
import os.path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from vertex import *
from GraphV2 import *
from deikstra import *
from test import *
''' Список Дел
1.Сделать граф крупнее, сместить в левый нижний угол ГОТОВО
2.Текст разбить по шагам ГОТОВО
3.Веса крупнее и другим цветом ГОТОВО
? - 4. Шаг назад
1 - 5. Сделать тест
Изменять кол-во вершин не закрывая прогу+Реализовать проверку вводимого текста(Гарантировать целые числа в LineEdit)
Чтобы считало длину кратчайшего пути и выводило остовное дерево списком вершин
'''

#обращение к файлу для чтения
FileToRead="input2.txt"

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(None)
        self.initUI() #подвязка интерфейса
        self.D=Deikstra(self.gr,self.Nodes,self.Start,self.Finish,self.table,self.lbl,self.lbl2,self.lbl3) #подвязка структуры для алгоритма
        self.but1.clicked.connect(self.stp) #шаг обхода графа
        self.but2.clicked.connect(self.rst) #сброс обхода 
        self.but3.clicked.connect(self.update_gr) #рбновить граф
        self.but4.clicked.connect(self.goAhead)
        self.but5.clicked.connect(self.goBack)
        self.but6.clicked.connect(self.openTest)
        self.showhints() #надписи на ребрах
    #реализация надписей над ребрами
    def showhints(self):
        for i in range(self.D.n-1,0,-1): #идем по вершинам от последней к всем остальным без повтора
            for j in range(i):
                leng=self.table.item(j,i).text() #берем значение веса из таблицы смежности
                if leng=="0": #если вес=0 то надписи нет
                    leng=""
                self.D.hints[""+str(j+1)+str(i+1)].label=QLabel(leng,self) #отрисовка текста
                self.D.hints[""+str(j+1)+str(i+1)].label.setStyleSheet("color:darkviolet;font-size: 18pt")
                self.D.hints[""+str(j+1)+str(i+1)].label.setGeometry(self.D.hints[""+str(j+1)+str(i+1)].x,self.D.hints[""+str(j+1)+str(i+1)].y-37,200,50) #положение текста
   #интерфейс
    def initUI(self):
        self.resize(1030, 820) #размеры окна
        self.drawtable() #отрисовка таблицы
        self.but1=QPushButton("Шаг обхода графа",self)
        self.but1.setGeometry(600,10,200,50)
        self.but2=QPushButton("Сбросить обход",self)
        self.but2.setGeometry(600,70,200,50)
        self.but3=QPushButton("Обновить граф",self)
        self.but3.setGeometry(600,130,200,50)
        self.but4=QPushButton("Далее",self)
        self.but4.setGeometry(600,190,200,50)
        self.but5=QPushButton("Назад",self)
        self.but5.setGeometry(320,190,200,50)
        self.but5.hide()
        self.but6=QPushButton("Перейти к тесту",self)
        self.but6.setGeometry(600,250,200,50)
        self.lbl=QLabel("Тут будут веса",self)
        self.lbl.setGeometry(320,220,200,50)
        self.lbl2=QLabel("Тут будут вершины",self)
        self.lbl2.setGeometry(320,240,200,50)
        self.lbl3=QLabel("Тут будет остовное дерево",self)
        self.lbl3.setGeometry(320,260,200,75)
        self.lbl3.setWordWrap(True)
        self.leN=QLineEdit(str(self.Nodes),self)
        self.leN.setGeometry(320,10,200,50)
        self.leF=QLineEdit(str(self.Start),self)
        self.leF.setGeometry(320,70,200,50)
        self.leT=QLineEdit(str(self.Finish),self)
        self.leT.setGeometry(320,130,200,50)
#        self.vert=Vertex(1,2,40)
        self.gr=Graph(self.matr) #отрисовка графа приходящего из файла GraphV2 на основе отосланной таблицы
        self.updateitems() #обновление значений таблицы и симметрия
        self.theory=['''Алгоритм Дейкстры находит кратчайшие пути от заданной вершины s до всех остальных в графе без ребер отрицательного веса.
Заведём массив d, в котором для каждой вершины v будем хранить текущую длину dv кратчайшего пути из s в v. Изначально ds=0, а для всех остальных вершин расстояние равно бесконечности (или любому числу, которое заведомо больше максимально возможного расстояния).
Во время работы алгоритма мы будем постепенно обновлять этот массив, находя более оптимальные пути к вершинам и уменьшая расстояние до них. Когда мы узнаем, что найденный путь до какой-то вершины v оптимальный, мы будем помечать эту вершину, поставив единицу (av=1) в специальном массиве a, изначально заполненном нулями.
Сам алгоритм состоит из n итераций, на каждой из которых выбирается вершина v с наименьшей величиной dv среди ещё не помеченных.''','''  
На первой итерации выбрана будет стартовая вершина s.
Выбранная вершина отмечается в массиве a, после чего из вершины v производятся релаксации: просматриваем все исходящие рёбра (v, u) и для каждой такой вершины u пытаемся улучшить значение du, выполнив присвоение:
где w — длина ребра (v, u).
На этом текущая итерация заканчивается, и алгоритм переходит к следующей: снова выбирается вершина с наименьшей величиной d, из неё производятся релаксации, и так далее. После n итераций, все вершины графа станут помеченными, и алгоритм завершает свою работу.
Корректность алгоритма определяется выполнением следующего утверждения. После того, как какая-либо вершина v становится помеченной, текущее расстояние до неё dv уже является кратчайшим, и, соответственно, больше меняться не будет. 
''','''Шаг 1. Перед началом выполнения алгоритма все вершины и 
дуги не окрашены. Каждой вершине присваивается число, 
равное длине кратчайшего пути из s в x, включающего только 
окрашенные вершины.
Пусть d(s) = 0, d(x)=∞ для всех вершин x, отличных от s. 
Окрасить вершину s и положить y = s.''',''' 
Шаг 2. Для каждой неокрашенной вершины х пересчитать 
величину d(x), выбрав минимальный вес ребра из предложенных.
Если d(x)=∞ для всех неокрашенных вершин х, закончить 
процедуру алгоритма: в исходном графе отсутствуют пути из s в 
неокрашенные вершины. В противном случае окрасить ту из вершин
х, для которой величина d(x) является наименьшей, а также окрасить 
дугу, ведущую в выбранную на данном шаге вершину x. 
Положить у = х.''','''
Шаг 3. Если у = t, закончить процедуру алгоритма: кратчайший 
путь из вершины s в вершину t найден (это единственный путь из s в t, 
составленный из окрашенных дуг). В противном случае перейти к 
шагу 2.
Окрашенные дуги образуют в исходном графе ориентированное 
дерево с корнем в вершине s. Это дерево называется
ориентированным деревом кратчайших путей.''']
        self.theoryLN=len(self.theory)-1 
        self.CurPag=0
        self.soprovod=QLabel(self.theory[0],self)
        self.soprovod.setStyleSheet("font-size: 13pt")
        self.soprovod.setGeometry(420,310,480,450)
        self.soprovod.setWordWrap(True) #авто-перенос слова на новую строку
    def openTest(self):
        self.w = TestWindow()
        self.w.show()
        self.hide()

    #шаг вперед в теории
    def goAhead(self):
        if self.CurPag==0:
            self.but5.show()
        if self.CurPag!=self.theoryLN:
            self.CurPag+=1
            self.soprovod.setText(self.theory[self.CurPag])
            self.update()
        if self.CurPag==self.theoryLN:
            self.but4.hide()
    #шаг назад в теории
    def goBack(self):
        if self.CurPag==self.theoryLN:
            self.but4.show()
        if self.CurPag!=0:
            self.CurPag-=1
            self.soprovod.setText(self.theory[self.CurPag])
            self.update()
        if self.CurPag==0:
            self.but5.hide()
    # геометрия таблицы и заполнение
    def drawtable(self):
        self.table=QTableWidget(self)
        self.table.setGeometry(10,10,277,285)
        self.data=self.readfile(FileToRead)
        if self.data:
            self.Nodes=int(self.data[0][:-1].split()[0]) #получаем количетво вершин из файла
            self.Start=int(self.data[0][:-1].split()[1]) #получаем стартовую вершину из файла
            self.Finish=int(self.data[0][:-1].split()[2]) #получаем финишную вершину из файла
            if self.Nodes!=0:
                self.table.setColumnCount(self.Nodes)
                self.table.setRowCount(self.Nodes)
                for x in range(self.Nodes):
                    self.table.setRowHeight(x,50) #размеры ячейки
                    self.table.setColumnWidth(x,50)
                    for y in range(self.Nodes):
                        print(x,y)
                        self.table.setItem(x,y,QTableWidgetItem()) #указываем каждую ячейку как самостоятельную единицу
                        self.table.item(x,y).setBackground(QColor(169,112,217)) #заливка ячеек
                        if y<=x: #блокировка ячеек ниже главной диагонали включая ее
                            self.table.item(x, y).setFlags(Qt.ItemIsEnabled) 
                self.filltable(self.data) #заполнение таблицы
    #заполнение таблицы
    def filltable(self,data):
        if type(data)==bool:
            return
        elif type(data)==list:
            self.matr=[] #если некорректно дан файл то не рисуем
            for x in range(self.Nodes):
                line=data[x+1][:-1].split() #для каждой вершины получаем веса связи и добавляем в список
                self.matr.append(line)
                for y in range(self.Nodes):
                    self.matr[x][y]=int(self.matr[x][y]) #текст в число
                    self.table.item(x,y).setText(str(line[y]))
        for x in range(self.Nodes):
            for y in range(self.Nodes):
                if y>x:self.table.item(y,x).setText(self.table.item(x,y).text()) #вставляем значения в ячейки если таблица симметрична
                self.matr[x][y]=int(self.matr[x][y])
        self.table.itemChanged.connect(self.updateitems) #обновление значений при изменении ячейки
    #обновление значений
    def updateitems(self):
        for x in range(self.Nodes):
            for y in range(self.Nodes):
                print(x,y)
                if y>x:self.table.item(y,x).setText(self.table.item(x,y).text()) #задаем симметричность
                self.gr.matr[x][y]=int(self.table.item(y,x).text())
    #рисование всего что связано с графом
    def paintEvent(self,event):
        self.pq = QPainter()
        self.pq.begin(window)
        self.pq.setFont(QFont('Decorative', 15))
        self.pq.setRenderHint(QPainter.Antialiasing)
        self.gr.draw_graph(self.pq,self.Nodes)
        self.pq.end()
    #обнуление графа
    def rst(self):
        self.D.reset()
        self.update()
    #шаг обхода графа
    def stp(self):
        self.D.step()
        self.update()
    #чтение из тхт-ка если нет то окно ошибки
    def readfile(self,filename):
        if os.path.exists(filename):
            return open(filename,'r').readlines()
        else: 
            msg = QMessageBox()
            msg.setWindowTitle("ERROR!!!")
            msg.setText("CANT READ FILE BECAUSE IT DOESNT EXIST")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return False
    #обновление графа  
    def update_gr(self):
        self.updateFromLines()
        self.gr.draw_graph(self.pq,self.Nodes)
        self.rst()
        for i in range(self.D.n-1,0,-1):
            for j in range(i):
                leng=self.table.item(j,i).text()
                if leng=="0":
                    leng=""
                print(i,j)
                self.D.hints[""+str(j+1)+str(i+1)].label.setText(leng)
        for key in self.D.hints.keys():
                self.D.hints[key].label.show()
    def updateFromLines(self):
        temp1=self.Start
        temp2=self.Finish
        temp3=self.Nodes
        try:
            self.Start=int(self.leF.text())
            self.Finish=int(self.leT.text())
            self.Nodes=int(self.leN.text())
        except:
                self.Start=temp1
                self.Finish=temp2
                self.Nodes=temp3
        self.D.s=self.Start
        self.D.f=self.Finish
        self.D.n=self.Nodes
        self.table.setColumnCount(self.Nodes)
        self.table.setRowCount(self.Nodes)
        if temp3==self.Nodes:
            pass
        elif temp3<self.Nodes:
            for i in range(self.Nodes):
                if i+1>len(self.matr):                    
                    self.matr.append([])
                while len(self.matr[i])<self.Nodes:
                    self.matr[i].append(0)
            print(self.matr)
            self.table.itemChanged.disconnect()
            for x in range(self.Nodes):
                for y in range(self.Nodes):
                        self.matr[x][y]=int(self.matr[x][y]) #текст в число
                        self.table.setItem(x,y,QTableWidgetItem()) #указываем каждую ячейку как самостоятельную единицу
                        self.table.item(x,y).setBackground(QColor(169,112,217)) #заливка ячеек
                        if y<=x: #блокировка ячеек ниже главной диагонали включая ее
                            self.table.item(x, y).setFlags(Qt.ItemIsEnabled) 
                        self.table.item(x,y).setText(str(self.matr[x][y]))
            self.table.itemChanged.connect(self.updateitems) #обновление значений при изменении ячейки
            for key in self.D.hints.keys():
                self.D.hints[key].label.hide()
            self.D.inithints()
            self.showhints()
        elif temp3>self.Nodes:
            for key in self.D.hints.keys():
                self.D.hints[key].label.hide()
            self.D.inithints()
            self.showhints()
        self.gr=Graph(self.matr)
        self.D.gr=self.gr
        

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


