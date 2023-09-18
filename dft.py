from copy import deepcopy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
#логика алгоритма и обработки данных
class D1eikstra:

    def __init__(self,gr,nodes,start,finish,table):

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
                    val=int(self.table[i][y])
                    if val>0 and y!=i:
                        self.distances[i+1][y+1]=val
        
        self.dfsfa=deepcopy(self.dfs)
        self.dfs[self.s-1]=0
        self.dfsfa[self.s-1]=0
        self.visited=[]
        self.inithints()
    #инициализация подсказок над ребрами 
    def inithints(self,x=0,y=0):
        if x!=0:
            x0=x
        else:
            x0=200
        if y!=0:
            y0=y
        else:
            y0=600
        self.hints={}
        r=140
        coords=[]
        for i in range(self.n):
            fi=(2*math.pi*i)/self.n
            coords.append([round(x0+r*math.cos(fi)),round(y0+r*math.sin(fi))])
        for i in range(len(coords)-1,0,-1):
            for j in range(i):
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
                    val=int(self.table[i][y])
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
        while min(self.dfs)!=float("inf"):
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
            self.visited.append(node+1)
            self.dfs[node]=float("inf")
            node=self.dfs.index(min(self.dfs))
            if min(self.dfs)!=float('inf'):
                node=self.dfs.index(min(self.dfs))
        self.answer=self.dfsfa[self.f-1]
                        
    #тут храняться надписи над ребрами
class hint():
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y

        

            
            