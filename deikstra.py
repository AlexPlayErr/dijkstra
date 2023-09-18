from copy import deepcopy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
#логика алгоритма и обработки данных
class Deikstra:

    def __init__(self,gr,nodes,start,finish,table:QTableWidget,lable:QLabel,lable2:QLabel,lable3:QLabel):
        self.lbl=lable
        self.lbl2=lable2
        self.lbl3=lable3
        self.table=table
        self.n=nodes
        self.gr=gr
        self.nodes=[]
        self.distances = {}
        self.dfs=[]
        self.s=start
        self.f=finish
        for i in range(self.n): #считывание из таблицы всех расстояний и составление словаря этих расстояний
            self.nodes.append((i+1))            
            self.distances[i+1]={}
            self.dfs.append(float("inf"))
            for y in range(self.n):
                    val=int(self.table.item(i,y).text())
                    if val>0 and y!=i:
                        self.distances[i+1][y+1]=val
        
        self.dfsfa=deepcopy(self.dfs)
        self.dfs[self.s-1]=0
        self.dfsfa[self.s-1]=0
        self.visited=[]
        self.inithints()
    #инициализация подсказок над ребрами 
    def inithints(self):
        self.hints={}
        x0=200
        y0=600
        r=140
        coords=[]
        for i in range(self.n):
            fi=(2*math.pi*i)/self.n
            coords.append([round(x0+r*math.cos(fi)),round(y0+r*math.sin(fi))])
        print(coords)
        for i in range(len(coords)-1,0,-1):
            for j in range(i):
                print(i,j)
                self.hints[""+str(j+1)+str(i+1)]=hint(round((coords[i][0]+coords[j][0])/2),round((coords[i][1]+coords[j][1])/2))
    #обнуление обхода графа - вызов в майн
    def reset(self):
        self.nodes=[]
        self.distances = {}
        self.dfs=[]
        for i in range(self.n):
            self.nodes.append((i+1))            
            self.distances[i+1]={}
            self.dfs.append(float("inf"))
            for y in range(self.n):
                    val=int(self.table.item(i,y).text())
                    if val>0 and y!=i:
                        self.distances[i+1][y+1]=val
        self.dfsfa=deepcopy(self.dfs)
        self.dfs[self.s-1]=0
        self.dfsfa[self.s-1]=0
        self.visited=[]
        for i in range(self.n):
            self.gr.vert_list[i].color=QColor(206,206,206)
        #изменение цвета на зеленый
    def changecolor(self,n):
        self.gr.vert_list[n].color=QColor(78, 212, 78)
    #шаг обхода
    def step(self):
        node=self.dfs.index(min(self.dfs))
        dists=""
        ver=""
        for dir in self.distances[node+1].keys():
            #заполнение лаблов текущих весов и текущих вершин
            if dir not in self.visited:
                ver=ver+str(dir)+","
                dists=dists+str(self.distances[node+1][dir])+","
            if dir not in self.visited and self.dfsfa[dir-1]>(self.distances[node+1][dir]+self.dfsfa[node]):
                self.dfs[dir-1]=self.distances[node+1][dir]+self.dfsfa[node]
                self.dfsfa[dir-1]=self.distances[node+1][dir]+self.dfsfa[node]
        self.lbl.setText("["+dists+"]")
        self.lbl2.setText("["+ver+"]")
        if node+1==self.s:
            self.lbl3.setText(str(node+1))
        else:
            self.lbl3.setText(self.lbl3.text()+"-"+str(node+1))
        self.changecolor(node)
        self.visited.append(node+1)
        self.dfs[node]=float("inf")
        if min(self.dfs)==float("inf"):
            self.lbl3.setText(self.lbl3.text()+"    Сумма весов кратчайшего пути из "+str(self.s)+" в "+str(self.f)+": "+str(self.dfsfa[self.f-1]))
            msg = QMessageBox() #если достигнут последний узел - то предупреждение
            msg.setWindowTitle("Signal")
            msg.setText("LAST POINT REACHED")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
       
        node=self.dfs.index(min(self.dfs))
        if min(self.dfs)!=float('inf'):
            node=self.dfs.index(min(self.dfs))
            self.gr.vert_list[node].color=QColor(221,78,46)
#тут храняться надписи над ребрами
class hint():
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y

        

            
            