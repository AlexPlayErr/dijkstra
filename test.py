import sys
from random import randint
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from copy import deepcopy
from dft import *
from Gft import *


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pq = QPainter()
        self.pq.begin(self)
        self.setWindowTitle("Test")
        self.initUI()
        self.initTest()
        self.task6()

    def initUI(self):
        self.resize(500, 350)
#         self.task=QLabel('''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
# Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
# Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
# Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
# Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
# ''',self)
        self.task=QLabel(''' Тут будет текст задания. Вы готовы начать тест?''',self)
        self.task.setGeometry(10,60,480,100)
        self.task.setWordWrap(True)
        #-------------------------------------------------------------------------------------------------
        self.CountLabel=QLabel("",self)
        self.CountLabel.setGeometry(390,10,110,40)
        #-------------------------------------------------------------------------------------------------
        self.taskCounter=0
        self.changeCounter()
        self.contBut=QPushButton("Продолжить",self)
        self.contBut.setGeometry(325,270,100,50)
        self.contBut.clicked.connect(self.contButPush)
        #-------------------------------------------------------------------------------------------------
        self.cb1=QCheckBox("Ответ 1",self)        
        self.cb2=QCheckBox("Ответ 2",self)
        self.cb3=QCheckBox("Ответ 3",self)    
        #-------------------------------------------------------------------------------------------------
        self.cb1.setGeometry(50,180,200,45)    
        self.cb2.setGeometry(50,230,200,45)   
        self.cb3.setGeometry(50,280,200,45)
        #-------------------------------------------------------------------------------------------------
        self.cbs=[self.cb1,self.cb2,self.cb3]
        for i in range(3):
            self.cbs[i].hide()
        #-------------------------------------------------------------------------------------------------
    def contButPush(self): 
        if self.taskCounter==0:
            for i in range(3):
                self.cbs[i].show()
        if self.taskCounter<4:
                if self.taskCounter>0:
                    self.checkAns()
                if len(self.tsList)>1:
                    chosentask=self.tsList[randint(0,len(self.tsList)-1)]
                    print(self.tsList, chosentask)
                    self.tsList.remove(chosentask)
                else:
                    chosentask=self.tsList[0]
                self.taskCounter+=1
                self.changeCounter()
            
                self.task.setText(self.tasks[chosentask]["task"])
                self.rghtans=list(self.tasks[chosentask]["rans"])
                for i in range(3):
                    self.cbs[i].setText(self.tasks[chosentask]["answers"][i+1])
        elif self.taskCounter==4:
            if self.taskCounter>0:
                    self.checkAns()
            self.taskCounter+=1
            self.changeCounter()
            for i in range(3):
                self.cbs[i].hide()
            self.task6()
            self.D.inithints(150,200)
            self.showhints()
            self.update_gr()
            self.D.step()
            self.task.setGeometry(350,25,100,160)
            self.task.setText("Сколько весит кратчайший путь из "+str(self.D.s )+" в "+str(self.D.f))
            print("Откуда: "+str(self.D.s),"Куда: "+str(self.D.f),"Вес: "+str(self.D.answer))
            self.lineans=QLineEdit(self)
            self.lineans.setPlaceholderText("Введите ответ сюда")
            self.lineans.setValidator(QIntValidator())
            self.lineans.setGeometry(325,210,150,25)
            self.lineans.show()
        elif self.taskCounter==5:
            if len(self.lineans.text())!=0:
                if int(self.lineans.text())==self.D.answer:
                    self.score+=1
            self.lineans.hide()
            self.contBut.hide()
            self.task.setText("Тест пройден! Ваша оценка: "+str(self.score)+"\n Позовите преподавателя для засчитывания ответа.")
    def checkAns(self):
        ans=[]
        for i in range(3):
            state=self.cbs[i].isChecked()
            if state:
                ans.append(i+1)
        print(ans,self.rghtans)
        if ans==self.rghtans:
            self.score+=1
        print(self.score)
        self.resetChecks()

    def resetChecks(self):
        for i in range(3):
            self.cbs[i].setChecked(False)
    
    def changeCounter(self):
        self.CountLabel.setText("Номер задания: "+str(self.taskCounter)+"/5")
    def initTest(self):
        self.score=0
        self.tasks={
            1:{
                "task":"Обновление меток носит название ",
                "answers":{1:"Конкатенация",2:"Унификация",3:"Релаксация"},
                "rans":[3]
            },
            2:{
                "task":"Работа алгоритма Дейкстры завершашется тогда, когда ",
                "answers":{1:"не осталось взвешенных \nподдеревьев",2:"найдено минимальное \nостовное дерево",3:"когда посещены\n все вершины"},
                "rans":[3]
            },
            3:{
                "task":"Какие требования к графу выдвигаются алгоритмом Дейкстры? ",
                "answers":{1:"граф должен быть взвешенным",2:"граф не должен иметь дуг \nотрицательного веса",3:"граф должен быть терминальным"},
                "rans":[1,2]
            },
            4:{
                "task":"Для чего предназначен алгоритм Дейкстры? ",
                "answers":{1:"для формирования минимального \nостовного дерева",2:"для нахождения кратчайшего \nрасстояния от одной из вершин \nграфа до всех остальных",3:"для поиска смежных вершин \nвзвешенного графа"},
                "rans":[2]
            },
            5:{
                "task":"Сложность алгоритма Дейкстры зависит: ",
                "answers":{1:"от способа нахождения вершины",2:"от способа обновления меток",3:"от способа хранения множества\n непосещенных вершин"},
                "rans":[1,2,3]
            }
        }
        self.tsList=[]
        for i in range(len(self.tasks)):
            self.tsList.append(i+1)
#---------------------------------------------------------------------------
    def genMatr(self):
        self.matr=[]
        for x in range(self.Nodes):
            line=[0,0,0,0,0]
            self.matr.append(line)
        for x in range(self.Nodes):
            for y in range(x):
                self.matr[x][y]=randint(0, 10)
                self.matr[y][x]=self.matr[x][y]
    def paintEvent(self,event):
        self.pq = QPainter()
        self.pq.begin(self)
        self.pq.setFont(QFont('Decorative', 15))
        self.pq.setRenderHint(QPainter.Antialiasing)
        self.gr.draw_graph(self.pq,self.Nodes)
        self.pq.end()

    def task6(self):
        self.Nodes=5
        self.Start=randint(1,5)
        self.Finish=self.Start
        while self.Finish==self.Start:
            self.Finish=randint(1,5)
        self.genMatr()
        self.gr=Graph1(self.matr)
        self.D=D1eikstra(self.gr,self.Nodes,self.Start,self.Finish,self.matr)

    def rst(self):
        self.D.reset()
        self.update()
    def update_gr(self):
        self.gr.draw_graph(self.pq,self.Nodes,150,200)
        self.rst()
        for i in range(self.D.n-1,0,-1):
            for j in range(i):
                leng=str(self.matr[j][i])
                if leng=="0":
                    leng=""
                print(i,j)
                self.D.hints[""+str(j+1)+str(i+1)].label.setText(leng)
        for key in self.D.hints.keys():
                self.D.hints[key].label.show()




    def showhints(self):
        for i in range(self.D.n-1,0,-1): #идем по вершинам от последней к всем остальным без повтора
            for j in range(i):
                leng=str(self.matr[i][j]) #берем значение веса из таблицы смежности
                if leng=="0": #если вес=0 то надписи нет
                    leng=""
                self.D.hints[""+str(j+1)+str(i+1)].label=QLabel(leng,self) #отрисовка текста
                self.D.hints[""+str(j+1)+str(i+1)].label.setStyleSheet("color:darkviolet;font-size: 18pt")
                self.D.hints[""+str(j+1)+str(i+1)].label.setGeometry(self.D.hints[""+str(j+1)+str(i+1)].x,self.D.hints[""+str(j+1)+str(i+1)].y-37,200,50) #положение текста        
    




#--------------------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())