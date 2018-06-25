from __future__ import unicode_literals
import sys
from PyQt4 import QtGui,QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import arange, sin, pi
import os
import random
from matplotlib.backends import qt_compat
import pandas as pd
import math
import numpy as np
from math import exp
from numpy import linalg as la
import os,time
import re
from snownlp import SnowNLP
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
import requests
import unittest
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import json
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool, Manager
import pickle
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore
class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setGeometry(50,50,1500,844)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Movie Analysis Tool")
        self.creatMenuBar()
        self.main_widget = QtGui.QWidget(self)
        self.mainPage = QtGui.QHBoxLayout(self.main_widget)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        #self.statusBar().showMessage("All hail matplotlib!", 2000)
        self.movieList=self.classPrep("classfinal.txt")
        self.movies1=list(self.movieList[self.movieList.class1==1][self.movieList.rating>"6"]["movie"].values)
        self.movies2=list(self.movieList[self.movieList.class2==1][self.movieList.rating>"6"]["movie"].values)
        self.movies3=list(self.movieList[self.movieList.class3==1][self.movieList.rating>"6"]["movie"].values)
        self.movies4=list(self.movieList[self.movieList.class4==1][self.movieList.rating>"6"]["movie"].values)
        self.movies5=list(self.movieList[self.movieList.class5==1][self.movieList.rating>"6"]["movie"].values)
        self.movies6=list(self.movieList[self.movieList.class6==1][self.movieList.rating>"6"]["movie"].values)
        self.movies7=list(self.movieList[self.movieList.class7==1][self.movieList.rating>"6"]["movie"].values)
        self.movieinformation= self.movieInforPrep("onlycompletefinal.txt")
        self.sample=self.getData("sampletest.txt")
        self.value=0
        self.userName=self.randomUser()
    def creatMenuBar(self):
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Home Page', self.home, 
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_A)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        
        self.menuBar().addMenu(self.file_menu)
        self.dataAnalysisMenu=QtGui.QMenu('&Data Analysis',self)
        self.algorithmAnalysis=QtGui.QMenu('&Algorithm Analysis',self)
        self.movieRecommend=QtGui.QMenu('Personal Recommendation',self)
        self.webCrawler=QtGui.QMenu('Web Crawler',self)
        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.dataAnalysisMenu)
        self.dataAnalysisMenu.addAction('&Douban & Weibo', self.dWFunction)
        self.dataAnalysisMenu.addAction('&Movie Analysis', self.movie)
        #self.dataAnalysisMenu.addAction('&Negative Weibo Analysis', self.negativeMovie)
        self.menuBar().addSeparator()
        #self.menuBar().addMenu(self.algorithmAnalysis)
        #self.algorithmAnalysis.addAction('&Algorithm Analysis', self.algorithm)
        #self.menuBar().addSeparator()
        self.menuBar().addMenu(self.movieRecommend)
        self.movieRecommend.addAction('&Movie Recommendation',self.recommendation)
        self.movieRecommend.addAction('&Movie in Theater', self.theater)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.webCrawler)
        self.webCrawler.addAction('&Web Crawler',self.weiboCrawler)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)
        self.menuBar().addSeparator()
        self.help_menu.addAction('&About', self.about)
    def fileQuit(self):
        self.close()
    def delete(self):
        for i in reversed(range(self.mainPage.count())): 
            self.mainPage.itemAt(i).widget().setParent(None)
    def home(self):
        self.delete()    
        self.palette=QtGui.QPalette()
        self.palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap("Movie-Night.jpg")))
        self.setPalette(self.palette)
    def dWFunction(self):
        self.delete()
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=80)
        sc.addDw()
        self.mainPage.addWidget(sc)
    def movie(self):
        self.delete()
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=80)
        sc.addNavigation()
        #st= MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=80)
        #st.addNavigation()
        self.mainPage.addWidget(sc)
        #self.mainPage.addWidget(st)
    def negativeMovie(self):
        self.delete()
        pass
    def algorithm(self):
        self.delete()
        pass
    def classPrep(self,fileName):
        header = ['movie_id','movie','rating','star','poster', 'class1', 'class2', 'class3','class4','class5','class6','class7']
        df = pd.read_csv(fileName, sep='\t', names=header)
        result=df.sort_values(['rating'],ascending=[0])
        return result
    def movieInforPrep(self,fileName):
        header = ['movie_id','movie','cast','rating','star', 'url1','poster']
        df = pd.read_csv(fileName, sep='\t', names=header)
        result=df.sort_values(['rating'],ascending=[0])
        return result
    def recommendation(self):
        self.delete()
        self.rebox=QtGui.QVBoxLayout(self)
        self.rewidget=QtGui.QWidget(self)
        self.rewidget.setLayout(self.rebox)
        self.rebutton=QtGui.QPushButton('START')
        self.rebutton.clicked.connect(self.sampling)
        self.mainPage.addWidget(self.rewidget)
        self.rebox.addWidget(self.rebutton)
        #self.sampling()
        
    def sampling(self):
        self.delete()
        #self.setStyleSheet("background-color: black;")
        self.palette=QtGui.QPalette()
        self.palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap("r10.jpg")))
        self.setPalette(self.palette)
        self.rebox=QtGui.QVBoxLayout(self)
        self.reboxbig=QtGui.QHBoxLayout(self)
        self.rewidget=QtGui.QWidget(self)
        self.rewidget.setStyleSheet("QWidget {color:#27a;font:20px;}")
        self.rewidget.setLayout(self.reboxbig)
        self.reboxbig.addLayout(self.rebox)
        empty=QtGui.QWidget()
        self.reboxbig.addWidget(empty)
        empty.setFixedWidth(500)
        empty.setFixedHeight(600)
        self.rewidget.setFixedWidth(800)
        self.rewidget.setFixedHeight(600)
        self.rebutton=QtGui.QPushButton('Rated')
        self.rebutton.clicked.connect(self.sampling)
        self.perbutton=QtGui.QPushButton('Recommedation')
        self.perbutton.clicked.connect(self.personal)
        movieList=self.movieList
        self.iLabel=QtGui.QLabel()
        #self.movieList
        
        self.itext=QtGui.QLabel()
        self.itext.setAlignment(QtCore.Qt.AlignCenter)
        self.rebox.addWidget(self.iLabel)
        self.rebox.addWidget(self.itext)
        self.recomboBox=QtGui.QComboBox(self)
        self.recomboBox.addItem('0')
        self.recomboBox.addItem('0.5')
        self.recomboBox.addItem('1.0')
        self.recomboBox.addItem('1.5')
        self.recomboBox.addItem('2.0')
        self.recomboBox.addItem('2.5')
        self.recomboBox.addItem('3.0')
        self.recomboBox.addItem('3.5')
        self.recomboBox.addItem('4.0')
        self.recomboBox.addItem('4.5')
        self.recomboBox.addItem('5.0')
        self.recomboBox.addItem('SKIP')
        self.rebox.addWidget(self.recomboBox)
        self.mainPage.addWidget(self.rewidget)
        self.rebox.addWidget(self.rebutton)
        self.rebox.addWidget(self.perbutton)
        classList=[['纪录片','战争', '历史','传记','武侠'],['动作','冒险',],['剧情','爱情','音乐','歌舞'],['科幻','奇幻'],['动画','儿童'],['悬疑', '惊悚','恐怖','犯罪','灾难'],['喜剧']]
        self.win=[0,0,0,0,0,0,0]
        self.false=[0,0,0,0,0,0,0]
        sample=[]
        for arm in range(0,len(classList)):
            sample.append((np.random.beta(self.win[arm]+1,self.false[arm]+1),arm))
        maxvalue,maxnum=max(sample)
            #print(maxnum)
        moviesample=self.randMovie(movieList,maxnum)
            #print("Do you like "+moviesample)
        posterurl=list(self.movieList[self.movieList.movie==moviesample]["poster"].values)[0]
        pixmap=QtGui.QPixmap(posterurl)
        self.iLabel.setPixmap(pixmap)
        self.iLabel.resize(pixmap.width(),pixmap.height())
        self.itext.setText(moviesample)
        self.recomboBox.activated[str].connect(self.comboboxvalue)
        #self.value=self.recomboBox.currentText()
        #print(self.value)
        #self.value=self.recomboBox.currentText()
        if self.value=="SKIP":
            moviesample=self.randMovie(movieList,maxnum)
                #print("Do you like "+moviesample)
            self.itext.setText(moviesample)
            self.value=self.recomboBox.currentText()
            print(self.value)
        elif float(self.value)>3:
            self.win[maxnum]+=1
            print(self.value)
        else:
            self.false[maxnum]+=1
            print(self.value)
        line=self.userName+"\t"+str(list(self.movieList[self.movieList.movie==moviesample]["movie_id"].values)[0])+"\t"+str(self.value)+"\t"+"2018"+"\t"+"05"+"\t"+"06"+"\t"+"sample"+"\n"
        self.writeFile("sampletest.txt",line)
    def randomUser(self):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        for i in range(10):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        return salt
    def comboboxvalue(self):
        self.value=self.recomboBox.currentText()
        return self.value
    def getData(self,fileName):
        header = ['user_id', 'movie_id', 'rating', 'year','month','day','comment']
        df = pd.read_csv(fileName, sep='\t', names=header)
        return df
    def writeFile(self,fileName,line):
        with open(fileName,'at',encoding='utf-8')as ft:
            ft.write(line)
            #print(user)
        ft.close()
    def userNegativeItem(self,userId):
        #sample=self.sample
        ratedList=list(self.sample[self.sample['user_id']==userId]['movie_id'].unique())
        unratedList=[i for i in set(self.sample['movie_id'].unique()) if i not in ratedList]
        popularity =[len(self.sample[self.sample['movie_id']==item]['user_id']) for item in unratedList]
        movies = pd.Series(popularity,index=unratedList)
        movies=movies.sort_values(ascending=False)
        return list(movies.index)[:len(ratedList)]
    def userPositiveItem(self,userId):
        #sample=self.sample
        movies=list(set(self.sample[self.sample['user_id']==userId]['movie_id']))
        return movies

    def initialDict(self,userId):
        #sample=self.sample
        positiveList=self.userPositiveItem(userId)
        negativeList=self.userNegativeItem(userId)
        dic={}
        for item in positiveList:
            dic[item]=self.sample[self.sample.user_id==userId][self.sample.movie_id==item]["rating"].values[0]
        for item in negativeList:
            dic[item]=0
        return dic   
    def inimodel(self,userID):
        inimodel={}
        #sample=self.sample
        for user in userID:
            userDict= self.initialDict(user)
            inimodel[user]=userDict
        return inimodel 
    def iniParaArray(self,userID,movieID,classCount):
        inip=np.random.rand(len(userID),classCount)
        iniq=np.random.rand(classCount,len(movieID))
        arrayP=pd.DataFrame(inip,columns=range(0,classCount),index=userID)
        arrayq=pd.DataFrame(iniq,columns=movieID,index=range(0,classCount))
        return arrayP,arrayq
    def userLists(self):
        #sample=self.sample
        return list(self.sample.user_id.unique())

    def movieLists(self):
        #sample=self.sample
        return list(self.sample.movie_id.unique())
    def sigmod(self,x):
        return 1.0/(1+exp(-x))
    def lfmCaculate(self,p,q,userId,movieId):
        p=np.mat(p.loc[userId].values)
        q=np.mat(q[movieId].values).T
        r=(p*q).sum()
        #r=self.sigmod(r)
        return r
    def lfModel(self,classCount,counts,alpha,lamda):
        userID=self.userLists()
        movieID=self.movieLists()
        p,q=self.iniParaArray(userID,movieID,classCount)
        iniModel=self.inimodel(userID)
        for i in range(0,counts):
            print(i)
            for user,userItem in iniModel.items():
                for movie,rui in userItem.items():
                    eui=rui-self.lfmCaculate(p,q,user,movie)
                    for c in range(0, classCount):
                        p[c][user]+=alpha*(eui*q[movie][c]-lamda*p[c][user])
                        q[movie][c]+=alpha*(eui*p[c][user]-lamda*q[movie][c])
                alpha*=0.9
        return p,q

    def recommend(self,p,q,userId,n):
        self.sample=self.getData("sampletest.txt")
        userList=self.userLists()
        movieList=self.movieLists()
        otherList=[movie for movie in movieList if movie not in userList]
        results=[(self.lfmCaculate(p,q,userId,movie), movie)for movie in otherList]
        results.sort()
        results.reverse()
        return results[:n]

    def sigmaPct(self,sigma,percentage=0.9):
        sumSigma=sum(sigma**2)
        squaSum=0
        num=0
        for i in sigma:
            squaSum+=i**2
            num+=1
            if squaSum>=sumSigma*percentage:
                return num
    def personal(self):
        self.delete()
        self.palette=QtGui.QPalette()
        self.palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap("r44.jpg")))
        self.setPalette(self.palette)
        self.sample=self.getData("sampletest.txt")
        p,q=self.lfModel(2,1,0.02,0.01)
        results=self.recommend(p,q,self.userName,5)
        print(results)
        self.pwidget=QtGui.QWidget(self)
        self.pbox=QtGui.QGridLayout(self)
        vbox=QtGui.QVBoxLayout(self)
        empty=QtGui.QWidget(self)
        vbox.addWidget(empty)
        vbox.addLayout(self.pbox)
        empty.setFixedHeight(150)
        empty.setFixedWidth(1500)
        self.pwidget.setLayout(vbox)
        self.pwidget.setFixedHeight=(530)
        count=0
        for i,j in results:
            print(j)
            titleText=self.movieList[self.movieList.movie_id==j]["movie"].values[0]
            url=self.movieList[self.movieList.movie_id==j]["poster"].values[0]
            smallmoviebox=QtGui.QWidget(self)
            smallmovie=QtGui.QVBoxLayout(self)
            smallmoviebox.setLayout(smallmovie)
            title=QtGui.QLabel(titleText)
            title.setAlignment(QtCore.Qt.AlignCenter)
            movieLabel=QtGui.QLabel()
            pixmap=QtGui.QPixmap(url)
            movieLabel.setPixmap(pixmap)
            movieLabel.resize(pixmap.width(),pixmap.height())
            smallmovie.addWidget(movieLabel)
            smallmovie.addWidget(title)
            self.pbox.addWidget(smallmoviebox,count//5,count%5)
            count=count+1
        self.mainPage.addWidget(self.pwidget)
        
    def randMovie(self,movieList,num):
        movieList=self.movieList
        movies1=self.movies1
        movies2=self.movies2
        movies3=self.movies3
        movies4=self.movies4
        movies5=self.movies5
        movies6=self.movies6
        movies7=self.movies7
        movies=""
        if num==0:
            movies=random.choice(movies1)
            movies1.remove(movies)
        if num==1:
            movies=random.choice(movies2)
        if num==2:
            movies=random.choice(movies3)
            movies3.remove(movies)
        if num==3:
            movies=random.choice(movies4)
            movies4.remove(movies)
        if num==4:
            movies=random.choice(movies5)
            movies5.remove(movies)
        if num==5:
            movies=random.choice(movies6)
            movies6.remove(movies)
        if num==6:
            movies=random.choice(movies7)
            movies7.remove(movies)
        for tt in [movies1,movies2,movies3,movies4,movies5,movies6,movies7]:
            try:
                tt.remove(movies)
            except:
                pass
        return movies

    def readFile(self,fileName):
        with open(fileName,'r',encoding='utf-8')as f:
            items = f.readlines()
        f.close()
        return items
    def theater(self):
        self.delete()
        self.palette=QtGui.QPalette()
        self.palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap("t1.jpg")))
        self.setPalette(self.palette)
        mainWidgetTheater=QtGui.QWidget(self)
        mainBoxTheater=QtGui.QVBoxLayout(self)
        mainWidgetTheater.setLayout(mainBoxTheater)
        titleBoxTheater=QtGui.QHBoxLayout(self)
        titleLabel=QtGui.QLabel("Now In Theater")
        titleLabel.setStyleSheet("QWidget {color:white;font: bold 50px;}")
        titleBoxTheater.addWidget(titleLabel)
        mainBoxTheater.addLayout(titleBoxTheater)
        #second = QtGui.QFrame(self)
        scrollAreaRight = QtGui.QScrollArea()  
        scrollAreaRight.setWidgetResizable(True)
        #scrollAreaRight.setWidget(second)
        #splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        #splitter.addWidget(scrollAreaRight)
        #splitter.setSizes([10, 100])
        mainBoxTheater.addWidget(scrollAreaRight)
        bigbox=QtGui.QWidget(self)
        movieWidget=QtGui.QWidget(self)
        movie=QtGui.QGridLayout(self)
        #scrollAreaRight.setLayout(movie)
        """
        change movies in theater information!!!!
        """
        movieTheater=self.readFile("new.txt")
        for i in range(0,len(movieTheater)):
            item=movieTheater[i]
            item=item.split("\t")
            titleText=item[0]+" "+item[1]
            url=item[-1].strip()
            smallmoviebox=QtGui.QWidget(self)
            smallmovie=QtGui.QVBoxLayout(self)
            smallmoviebox.setLayout(smallmovie)
            title=QtGui.QLabel(titleText)
            title.setStyleSheet("QWidget {color:white;font: bold 20px;}")
            movieLabel=QtGui.QLabel()
            pixmap=QtGui.QPixmap(url)
            movieLabel.setPixmap(pixmap)
            movieLabel.resize(pixmap.width(),pixmap.height())
            smallmovie.addWidget(movieLabel)
            smallmovie.addWidget(title)
            movie.addWidget(smallmoviebox,i//5,i%5)
            movie.setSpacing(0)
        movieWidget.setLayout(movie)
        movieWidget.setMinimumSize(1000,2000)
        scrollAreaRight.setWidget(movieWidget)
        #mainBoxTheater.addWidget(smallmoviebox)
        self.mainPage.addWidget(mainWidgetTheater)
    def weiboCrawler(self):
        self.delete()
        wei=weiboCrawler(self.main_widget)
        self.mainPage.addWidget(wei)
    def closeEvent(self, ce):
        self.fileQuit()
    def about(self):
        self.delete()
        QtGui.QMessageBox.about(self, "About",
                                """This is a research project to analysis users'

behaviour in social network.All data was used as

academic analysis without any comercial purpose.                                   

Copyright 2018 Shijie Zhang.
"""
                                )
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeperator()
            else:
                target.addAction(action)
    def createAction(self, text, slot=None, shortcut=None,
            tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        # a figure instance to plot on
        #self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        #self.canvas = FigureCanvas(self.figure)
    
        
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        #self.button = QtGui.QPushButton('Plot')
        #self.button.clicked.connect(self.plot)

        # set the layout
        #layout = QtGui.QVBoxLayout()
        #layout.addWidget(mainMenu)
        #layout.addWidget(self.toolbar)
        #layout.addWidget(self.canvas)
        #layout.addWidget(self.button)
        #self.setLayout(layout)
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=80):
        #self.main=FigureCanvas.QWidget()
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        #self.compute_initial_figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.main_widget = QtGui.QWidget(self)
        self.douban=self.doubanPrep("doubancommentnew.txt")
        self.weibo=self.sinaPrep("sentiment.txt")
        self.mainLayout =QtGui.QHBoxLayout(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.mainLayout.addLayout(self.layout)
        self.information=QtGui.QVBoxLayout(self)
        self.mainWidget=QtGui.QWidget()
        self.mainWidget.setLayout(self.information)
        self.mainWidget.setFixedWidth(650)
        self.mainLayout.addWidget(self.mainWidget)
        self.mainWidget.setStyleSheet("QWidget {color:#27a;background-color:#f2f7f6;}")
        #self.setLayout(layout)
    def addNavigation(self):
        self.canvas = FigureCanvas(self.fig)  
        weibo=self.weibo
        douban=self.douban
        layout=self.layout
        # this is the Navigation widget  
        # it takes the Canvas widget and a parent  
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plotMovie)
        self.buttoninfor=QtGui.QPushButton('Show Information')
        self.buttoninfor.clicked.connect(self.getMovieInformation)
        self.comboBox=QtGui.QComboBox(self)
        self.comboBoxYear=QtGui.QComboBox(self)
        layouth=QtGui.QHBoxLayout(self)
        layouth.addWidget(self.comboBox)
        layouth.addWidget(self.comboBoxYear)
        self.addComboBoxItem(self.comboBox,douban)
        self.comboBox.activated[str].connect(self.addComboBoxItemYear)
        #self.addComboBoxItemYear(self.comboBoxYear,douban,int(self.comboBox.currentText())) 
        layouth.addWidget(self.button)
        layouth.addWidget(self.buttoninfor)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(layouth)
        self.showInfor()
    def showInfor(self):
        self.titlebox=QtGui.QHBoxLayout(self)
        self.label=QtGui.QLabel("Movie(Year)")
        self.label.setStyleSheet("QWidget {font: bold 50px;}")
        self.titlebox.addWidget(self.label)
        self.inforbox=QtGui.QHBoxLayout(self)
        self.iLabel=QtGui.QLabel()
        self.inforbox.addWidget(self.iLabel)
        self.inforbox.setSpacing(10)
        pixmap=QtGui.QPixmap("p2519994468.jpg")
        self.iLabel.setPixmap(pixmap)
        self.iLabel.resize(pixmap.width(),pixmap.height())
        self.widget=QtGui.QWidget()
        self.infor =QtGui.QGridLayout(self)
        self.infor.setSpacing(10)
        self.inforbox.addWidget(self.widget)
        self.dlabel=QtGui.QLabel("Directors:")
        self.dlabel.setStyleSheet("QWidget {font: bold 18px;}")
        self.infor.addWidget(self.dlabel,0,0)
        self.dbox=QtGui.QLineEdit(self)
        self.dbox.setEnabled(False)
        self.dbox.setStyleSheet("QWidget {font: bold 18px;border:0px;}")
        self.infor.addWidget(self.dbox,0,1)
        self.clabel=QtGui.QLabel("Casts:")
        self.clabel.setStyleSheet("QWidget {font: bold 18px;}")
        self.infor.addWidget(self.clabel,1,0)
        self.cbox=QtGui.QLineEdit(self)
        self.cbox.setEnabled(False)
        self.cbox.setStyleSheet("QWidget {font: bold 18px;border:0px;}")
        self.infor.addWidget(self.cbox,1,1)
        self.glabel=QtGui.QLabel("Genres:")
        self.glabel.setStyleSheet("QWidget {font: bold 18px;}")
        self.infor.addWidget(self.glabel,2,0)
        self.gbox=QtGui.QLineEdit(self)
        self.gbox.setEnabled(False)
        self.gbox.setStyleSheet("QWidget {font: bold 18px;border:0px;}")
        self.infor.addWidget(self.gbox,2,1)
        self.ratinglabel=QtGui.QLabel("Rating:")
        self.ratinglabel.setStyleSheet("QWidget {font: bold 18px;}")
        self.infor.addWidget(self.ratinglabel,3,0)
        self.ratingbox=QtGui.QLineEdit(self)
        self.ratingbox.setEnabled(False)
        self.ratingbox.setStyleSheet("QWidget {font: bold 18px;border:0px;}")
        self.infor.addWidget(self.ratingbox,3,1)
        self.countrylabel=QtGui.QLabel("Country:")
        self.countrylabel.setStyleSheet("QWidget {font: bold 18px;}")
        self.infor.addWidget(self.countrylabel,4,0)
        self.countrybox=QtGui.QLineEdit(self)
        self.countrybox.setEnabled(False)
        self.countrybox.setStyleSheet("QWidget {font: bold 18px;border:0px;}")
        self.infor.addWidget(self.countrybox,4,1)
        summary=''
        #self.summ =QtGui.QGridLayout(self)
        #for i in range(0, len(summary)):
         #   button=QtGui.QLabel(summary[i])
          #  self.summ.addWidget(button,i//2,i%2)
        self.sslabel=QtGui.QTextEdit(summary)
        self.information.addLayout(self.titlebox)
        self.information.addLayout(self.inforbox)
        self.widget.setLayout(self.infor)
        self.widget.setFixedWidth(330)
        #self.information.addWidget(self.widget)
        self.information.addWidget(self.sslabel)
        self.sslabel.setEnabled(False)
        self.sslabel.setStyleSheet("QWidget { font:bold 20px;border:0px;color:#27a;background-color:#f2f7f6;}")
        self.information.addStretch(1)
        #self.widget.move()
    def getMovieInformation(self):
        movieid=self.comboBox.currentText()
        movie_info=requests.get('http://api.douban.com/v2/movie/subject/'+movieid).json()
        name=movie_info["title"]
        ratingM=movie_info["rating"]["max"]
        ratingA=movie_info["rating"]["average"]
        ratingMi=movie_info["rating"]["min"]
        stars=movie_info["rating"]["stars"]
        year=movie_info["year"]
        image=movie_info["images"]["small"]
        alt=movie_info["alt"]
        countries=movie_info["countries"]
        country=""
        for i in countries:
            country+=i+"\t"
        genres=movie_info["genres"]
        genre=""
        for i in genres:
            genre+=i+"\t"
        casts=movie_info["casts"]
        cast=""
        for j in casts:
            cast=j["name"]+"\t"
        summary=movie_info["summary"]
        directors=movie_info["directors"]
        director=""
        for k in directors:
            director+=k["name"]+"\t"
        poster_url=image=movie_info["images"]["small"].replace("webp","jpg").split("/")[-1]
        image="poster/"+image
        #pixmap=QtGui.QPixmap(os.getcwd()+image)
        #self.iLabel.setPixmap(pixmap)
        #self.resize(pixmap.width(),pixmap.height())
        self.label.setText(name+" ("+year+")")
        self.dbox.setText(director)
        self.cbox.setText(cast)
        self.gbox.setText(genre)
        self.ratingbox.setText(str(ratingA))
        self.countrybox.setText(country)
        self.sslabel.setText(summary)
        pixmap=QtGui.QPixmap(image)
        self.iLabel.setPixmap(pixmap)
        self.iLabel.resize(pixmap.width(),pixmap.height())
    def addDw(self):
        self.canvas = FigureCanvas(self.fig)  
        weibo=self.weibo
        douban=self.douban
        layout=self.layout
        # this is the Navigation widget  
        # it takes the Canvas widget and a parent  
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.weiboDouban)
        layouth=QtGui.QHBoxLayout(self)
        layouth.addWidget(self.button)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(layouth)
        lllabel=QtGui.QLabel()
        pixmap=QtGui.QPixmap("curve_fit.png")
        lllabel.setPixmap(pixmap)
        lllabel.resize(pixmap.width(),pixmap.height())
        summary="Each point in figure 1 represents the average movie rating in Douban and public sentiment rating in Weibo. As shown in figure1, data are mainly centred in a circular region and contain many singular points with relatively low sentiment rating, which illustrates that there is no relation between two datasets. "
        summary=summary+"Due to the incompleteness and error of text mining and data collection, the points with sentiment ratings below 2.5 are deleted and sentiment ratings were rescaled from interval [0, 1] to interval [0, 5] using linear equation.  The figure 2 is liner symmetric figure layout about y=x, which shows that Weibo and Douban are two corresponding social network datasets."
        ssslabel=QtGui.QTextEdit(summary)
        ssslabel.setStyleSheet("QWidget { font:bold 20px;border:0px;color:#27a;background-color:#f2f7f6;}")
        self.information.addWidget(lllabel)
        self.information.addWidget(ssslabel)
    def addComboBoxItemYear(self):
        douban=self.douban
        movieid=int(self.comboBox.currentText())
        itemList=list(douban[douban.movie_id==movieid].year.unique())
        itemList.sort()
        itemList.reverse()
        self.comboBoxYear.clear()
        for item in itemList:
            self.comboBoxYear.addItem(str(item))
    def addComboBoxItem(self,comboBox,douban):
        itemList=list(douban.movie_id.unique())
        for item in itemList:
            comboBox.addItem(str(item))
    def comoboxValue(self):
        return self.comboBox
    def readFile(self,fileName):
        with open(fileName,'r',encoding='utf-8')as f:
            items = f.readlines()
        f.close()
        return items
    def doubanPrep(self,fileName):
        header = ['user_id', 'movie_id', 'rating', 'year','month','day','comment']
        df = pd.read_csv(fileName, sep='\t', names=header)
        return df
    def sinaPrep(self,fileName):
        header = ['user_id', 'movie_id', 'year', 'month','day','rating','norRating']
        df = pd.read_csv(fileName, sep='\t', names=header)
        return df
    def ratings(self):
        list(sample[sample.user_id==userId][sample.movie_id==movie]['rating'].values)[0]
    def sigmod(self,x):
        return 1.0/(1+exp(-x))

    def dataPre(self,fileName):
        lists=readFile(fileName)
        for i in lists:
            i=i.split("\t")
            userId=i[0]
            movieId=i[1]
            rating=i[2]
            time=i[3].split(" ")[0].split("-")
            year=time[0]
            day=time[2]
            month=time[1]
            comment=i[4]
            line=userId+"\t"+movieId+"\t"+str(rating)+"\t"+year+"\t"+month+"\t"+day+"\t"+comment
            writeFile("doubanzhanlang.txt",line)  
    def writeFile(self,fileName,line):
        with open(fileName,'at',encoding='utf-8')as ft:
            ft.write(line)
            #print(user)
        ft.close()
    def userNumber(self,sample):
        return sample.user_id.unique().shape()[0]
    def userRating(self,douban,movieId,year,month,day):
        return list(douban[douban.movie_id==movieId][douban.year==year][douban.month==month][douban.day==day]["rating"].values)
    def aveMonth(self,douban,movieid,year,month):
        sumRatings=0
        ratings=list(douban[douban.movie_id==movieid][douban.year==year][douban.month==month]["rating"].values)
        for i in ratings:
            sumRatings+=sigmod(int(i)/10)
        if len(ratings)==0:
            return 0
        #print(sumRatings)
        #print(len(ratings))
        return sumRatings/len(ratings)

    def aveDay(self,douban,movieid,year,month,day):
        sumRatings=0
        ratings=list(douban[douban.movie_id==movieid][douban.year==year][douban.month==month][douban.day==day]["rating"].values)
        for i in ratings:
            sumRatings+=int(i)/10
        if len(ratings)==0:
            return 0,0
        #print(sumRatings)
        #print(len(ratings))
        return sumRatings/len(ratings), len(ratings)

    def aveWeibo(self,weibo,movieid,year,month,day):
        sumRatings=0
        ratings=list(weibo[weibo.movie_id==movieid][weibo.year==year][weibo.month==month][weibo.day==day]["norRating"].values)
        for i in ratings:
            sumRatings+=float(i)
            #print(sumRatings)
        if len(ratings)==0:
            return 0,0
        #print(sumRatings)
        #print(len(ratings))
        return sumRatings/len(ratings),len(ratings)

    def plotMovie(self):
        douban=self.douban
        weibo=self.weibo
        movieid=int(self.comboBox.currentText())
        year=int(self.comboBoxYear.currentText())
        date=list(range(1,13))
        day=list(range(1,31))
        ave1=[]
        num1=[]
        ave2=[]
        num2=[]
        count=1
        count2=1
        nnum1=[]
        nnum2=[]
        rate0, lenth0=self.aveDay(douban,movieid,year,1,1)
        ave1.append(rate0)
        nnum1.append(lenth0)
        num1.append("11")
        rate1, lenth1=self.aveDay(weibo,movieid,year,1,1)
        ave2.append(rate1)
        nnum2.append(lenth1)
        num2.append("11")
        for i in date:
            for j in day:
                rates, lenth=self.aveDay(douban,movieid,year,i,j)
                #print(rates,lenth)
                nnum1.append(lenth+nnum1[count-1])
                if nnum1[count]==0:
                    ave1.append(0)
                    num1.append(str(i)+str(j))
                if nnum1[count]!=0:
                    sumR=rates*lenth+ave1[count-1]*nnum1[count-1]
                    ave1.append(sumR/nnum1[count])
                    num1.append(str(i)+str(j))
                count=count+1            
        #print(ave1)       
        for ii in date:
            for jj in day:
                rates, lenth=self.aveWeibo(weibo,movieid,year,ii,jj)
                #print(rates,lenth)            
                nnum2.append(lenth+nnum2[count2-1])
                if nnum2[count2]==0:
                    ave2.append(0)
                    num2.append(str(ii)+str(jj))
                if nnum2[count2]!=0:
                    sumR2=rates*lenth+ave2[count2-1]*nnum2[count2-1]
                    ave2.append(sumR2/nnum2[count2])
                    num2.append(str(ii)+str(jj))
                count2=count2+1            
        #print(len(ave1),len(ave2))                   
        ax=self.figure.add_subplot(111)
        ax.clear()
        ave1=np.array(ave1)
        num1=np.array(list(range(0,count)))
        ave2=np.array(ave2)
        num2=np.array(list(range(0,count2)))
        #plt.scatter(num1,ave1,marker='x',color='m')
        plot1 = ax.plot(num1,ave1, 'o-',label='Douban values')
        plot2 = ax.plot(num2,ave2, 'r-',label='Weibo values')
        plt.xlabel('Time')
        plt.ylabel('Ratings')
        ax.legend()
        ax.grid(True)
        plt.title("Weibo VS Douban")
        #plt.axis([0,361,2,5])
        #plt.scatter(num2,ave2,marker='o',color='r')
        self.canvas.draw()
    def doubanAveg(self,douban,movieid):
        ratings=list(douban[douban.movie_id==movieid]["rating"].values)
        sumRatings=0
        for rating in ratings:
            sumRatings+=float(rating/10)
        if len(ratings)==0:
            return 0
        return sumRatings/len(ratings)
    def doubanAvegLen(self,douban,movieid):
        ratings=list(douban[douban.movie_id==movieid]["rating"].values)
        return len(ratings)
    def weiboAveg(self,weibo,movieid):
        ratings=list(weibo[weibo.movie_id==movieid]["rating"].values)
        sumRatings=0
        for rating in ratings:
            sumRatings+=float(rating)
        return sumRatings/len(ratings)
    """
    douban and weibo
    """
    def weiboDouban(self):
        douban=self.douban
        weibo=self.weibo
        weiboDouban=[]
        movieList=[]
        x=[]
        y=[]
        movieDouban=list(douban.movie_id.unique())
        movieWeibo=list(weibo.movie_id.unique())
        for i in movieDouban:
            if i in movieWeibo:
                movieList.append(i)
        #print(len(movieList))
        for i in movieList:
            d=self.doubanAveg(douban,i)
            #print(d)
            w=self.weiboAveg(weibo,i)
           # print(w)
            if w>0.5:
                x.append(d)
                y.append(w*25/3-10/3)
        ax=self.figure.add_subplot(111)
        x=np.array(x)
        y=np.array(y)
        sample=np.linspace(0,5,1000)
        sampley=[i+0.5 for i in sample]
        ax.scatter(x,y,marker='.',color='m')
        #plot1=plt.plot(x,y, 'r',label='polyfit values')
        plt.xlabel('Douban Ratings')
        plt.ylabel('Weibo Ratings')
        plt.legend()
        plt.title("Weibo VS Douban")
        ax.plot(sample,sample,'r',label='polyfit values')
        plt.axis([0,5,0,5])
        self.canvas.draw()
    """http://api.douban.com/v2/movie/subject/1764796"""
    def getMovieInfor(self,fileName):
        movies=[]
        lines=readFile(fileName)
        for line in lines:
            lines=line.split("\t")
            movieid=lines[0]
            print(movieid)
            movies.append(movieid)
            movie_info=requests.get('http://api.douban.com/v2/movie/subject/'+str(movieid)).json()
            #movieId=movie_info["id"]
            name=movie_info["title"]
            ratingM=movie_info["rating"]["max"]
            ratingA=movie_info["rating"]["average"]
            ratingMi=movie_info["rating"]["min"]
            stars=movie_info["rating"]["stars"]
            year=movie_info["year"]
            image=movie_info["images"]["small"]
            alt=movie_info["alt"]
            countries=movie_info["countries"]
            country=""
            for i in countries:
                country+=i+"/"
            genres=movie_info["genres"]
            genre=""
            for i in genres:
                genre+=i+"/"
            casts=movie_info["casts"]
            cast=""
            for j in casts:
                cast=j["name"]+"/"
            summary=movie_info["summary"]
            directors=movie_info["directors"]
            director=""
            for k in directors:
                director+=k["name"]+"/"
            detail=str(movieid)+"\t"+ name+"\t"+str(ratingM)+"\t"+str(ratingA)+"\t"+str(ratingMi)+"\t"+str(stars)+"\t"+str(year)+"\t"+image+"\t"+alt+"\t"+country+"\t"+genre+"\t"+cast+"\t"+director+"\t"+"\n"
            writeFile("movieInfor.txt",detail)
            sleep(3)

    #douban=doubanPrep("doubancommentnew.txt")
    #weibo=sinaPrep("sentiment.txt")
    def moviePre(self,douban,weibo,movieid,year):
        date=list(range(1,13))
        day=list(range(1,31))
        ave1=[]
        ave2=[]
        for i in date:
            for j in day:
                dou=aveDay(douban,movieid,year,i,j)
                wei=aveWeibo(weibo,movieid,year,i,j)
                if wei*dou>0:
                        ave1.append(dou)
                        ave2.append(wei)
        f1 = plt.figure(1)
        plt.subplot(211)
        ave1=np.array(ave1)
        #num1=np.array(num1)
        ave2=np.array(ave2)
        #num2=np.array(num2)
        plt.scatter(ave1,ave2,marker='o',color='r')
        #plt.scatter(num2,ave2,marker='o',color='r')
        plt.show()
    def negativeWeibo(self,weibo):
        movieWeibo=list(weibo.movie_id.unique())
        negativeList=[]
        for movie in movieWeibo:
            sentiment=weiboAveg(weibo,movie)
            if sentiment<0.6:
                negativeList.append((sentiment,movie))
        return negativeList
    def negativeDouban(self,weibo,douban):
        negativeList=negativeWeibo(weibo)
        negativeDouban=[]
        for i,j in negativeList:
            result=doubanAveg(douban,j)
            negativeDouban.append((result,doubanAvegLen(douban,j)))
        return negativeDouban
    def aveDoubanRating(self,douban):
        movieDouban=list(douban.movie_id.unique())
        sumRating=0
        for i in movieDouban:
            sumRating+=doubanAveg(douban,i)
        return sumRating/len(movieDouban)
    def ratingCount(self,douban,movieid):
        ratings=list(douban[douban.movie_id==movieid]["rating"].values)
        return len(ratings)
    def aveRatingCount(self,douban):
        movieDouban=list(douban.movie_id.unique())
        sumCount=0
        for i in movieDouban:
            sumCount+=ratingCount(douban,i)
        return sumCount/len(movieDouban)
    """
    sentiment vs count
    """
    def plotNegativeDouban(self,weibo,douban):
        negativeDouban=negativeDouban(weibo,douban)
        negativeWeibo=negativeWeibo(weibo)
        result=[]
        count=[]
        countFinal=[]
        sentiment=[]
        for sen,li in negativeWeibo:
            sentiment.append(sen)
        for i, j in negativeDouban:
            result.append(i/5)
            count.append(j)
        result=np.array(result)
        count=np.array(count)
        mean=np.mean(count)
        std=np.std(count)
        sentiment=np.array(sentiment)
        for i in count:
            countNew=(i-mean)/std
            countFinal.append(countNew)
        sample=np.linspace(0,5,1000)
        plot2=plt.plot(sample,sample,'r',label='polyfit values')
        plt.scatter(sentiment,countFinal,marker='o',color='m')
        plt.show()

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
        #
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)

   
    def sampleFunction(self):
        pass
class weiboCrawler(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self,parent=None)
        self.setWindowTitle('Weibo Crawler')
        self.weiboLayout=QtGui.QWidget(self)
        self.weiboBox=QtGui.QVBoxLayout(self)
        self.form=QtGui.QHBoxLayout(self)
        #self.weiboLayout.addWidget(self.weiboBox)
        self.addListView()
        self.weiboBox.addLayout(self.form)
        self.addform()
        self.weiboLayout.setLayout(self.weiboBox)
        self.weiboLayout.setFixedWidth(1300)
        self.weiboLayout.setFixedHeight(700)
        self.weiboLayout.move(90,30)
        self.weiboLayout.setStyleSheet("QWidget {font: bold 18px;color:#27a;background-color:#f2f7f6;}")
        #self.setCentralWidget(self.weiboLayout)
    def addListView(self):
        self.MyTable=QtGui.QTableWidget(1000,5)
        self.MyTable.setHorizontalHeaderLabels(['user','movie','time','comment','sentiment']) 
        newItem = QtGui.QTableWidgetItem()  
        self.MyTable.setItem(1, 0, newItem)    
        newItem = QtGui.QTableWidgetItem()  
        self.MyTable.setItem(1, 1, newItem)  
        newItem = QtGui.QTableWidgetItem()  
        self.MyTable.setItem(1, 2, newItem)
        self.weiboBox.addWidget(self.MyTable)
        self.MyTable.setColumnWidth(1,100)
        self.MyTable.setColumnWidth(2,100)
        self.MyTable.setColumnWidth(3,100)
        self.MyTable.setColumnWidth(4,100)
        self.MyTable.setColumnWidth(5,200)
    def addform(self):
        self.mlabel=QtGui.QLabel("Movie Name:")
        self.mtext=QtGui.QLineEdit(self)
        self.flabel=QtGui.QLabel("File Name:")
        self.ftext=QtGui.QLineEdit(self)
        self.start=QtGui.QPushButton("Start")
        self.restart=QtGui.QPushButton("Reset")
        self.form.addWidget(self.mlabel)
        self.form.addWidget(self.mtext)
        self.form.addWidget(self.flabel)
        self.form.addWidget(self.ftext)
        self.form.addWidget(self.start)
        self.form.addWidget(self.restart)
        self.start.clicked.connect(self.addTableFunction)
        self.restart.clicked.connect(self.restartFunction)
        for x in range(self.MyTable.columnCount()):  
            headItem = self.MyTable.horizontalHeaderItem(x)   #获得水平方向表头的Item对象  
            #headItem.setFont(textFont)                        #设置字体  
            headItem.setBackgroundColor(QtGui.QColor("#f2f7f6"))      #设置单元格背景颜色  
            headItem.setTextColor(QtGui.QColor("#f2f7f6"))
        
    def tttaddTableFunction(self):
        for count in range(0,100):
            rbox=QtGui.QLineEdit(self)
            rbox.setEnabled(False)
            rbox.setText(str(count))
            rbox.setStyleSheet("QWidget {font: bold 18px;border:0px;}")
            self.weiboBox.addWidget(rbox)
            #sleep(1)
    def fiill(self,count):
        user=str(4234587451724974)
        movieName=self.mtext.text()
        time="4小时前"
        comment="张翰更博，遥记得去年《战狼2》张翰的这句话承包了整个剧的笑点！"
        newItem = QtGui.QTableWidgetItem()  
        self.MyTable.setItem(count, 0, newItem)
        newItem.setText(user)
        newItem = QtGui.QTableWidgetItem()  
        self.MyTable.setItem(count, 1, newItem)
        newItem.setText(user)
        newItem = QtGui.QTableWidgetItem()  
        self.MyTable.setItem(count, 2, newItem)
        newItem.setText(user)
        newItem = QtGui.QTableWidgetItem()  
        self.MyTable.setItem(count, 3, newItem)
        newItem.setText(user)
            #result=SnowNLP(comment)
            #sentiment=str((result.sentiments)*5)
        newItem = QtGui.QTableWidgetItem("11")  
        self.MyTable.setItem(count, 4, newItem)
        #self.MyTable.show()
    def addTableFunction(self):
        #movieName="电影"+movieName
        movieName=self.mtext.text()
        movieid=self.ftext.text()
        i=2
        count=0
        wrong=requests.get('https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%E7%BE%9E%E7%BE%9E%E7%9A%84%E9%93%81%E6%8B%B3&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%BE%9E%E7%BE%9E%E7%9A%84%E9%93%81%E6%8B%B3&title=%E7%BE%9E%E7%BE%9E%E7%9A%84%E9%93%81%E6%8B%B3&containerid=100103type%3D1%26q%3D%E7%BE%9E%E7%BE%9E%E7%9A%84%E9%93%81%E6%8B%B3&page=50').json()
        url="https://m.weibo.cn/api/container/getIndex?type=all&queryVal="+movieName+"&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D"+movieName+"&title="+movieName+"&containerid=100103type%3D1%26q%3D"+movieName+"&page="+str(i)
        data=requests.get(url).json()
        while data["ok"]==1:
            url="https://m.weibo.cn/api/container/getIndex?type=all&queryVal="+movieName+"&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D"+movieName+"&title="+movieName+"&containerid=100103type%3D1%26q%3D"+movieName+"&page="+str(i)
            data=requests.get(url).json()
            with open(movieid+".txt",'at',encoding='utf-8')as ft:
                try:
                    js = data["data"]["cards"][0]["card_group"]
                    for jss in js:
                        Pattern=re.compile(u"<(.*)>")
                        line=''
                        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                        text=jss['mblog']['text'].translate(non_bmp_map)
                        if(len(Pattern.sub(r'',text))>=3):
                            line= str(jss['mblog']['id'])+'\t'+str(jss['mblog']['created_at'])+'\t'+str(Pattern.sub(r'',text))
                            user=str(jss['mblog']['id'])
                            time=jss['mblog']['created_at']
                            comment=Pattern.sub(r'',text)
                            #print(user)
                            #print(time)
                            #print(comment)
                            newItem = QtGui.QTableWidgetItem(user)  
                            self.MyTable.setItem(count, 0, newItem)    
                            newItem = QtGui.QTableWidgetItem(movieName)  
                            self.MyTable.setItem(count, 1, newItem)  
                            newItem = QtGui.QTableWidgetItem(time)  
                            self.MyTable.setItem(count, 2, newItem)
                            newItem = QtGui.QTableWidgetItem(comment)  
                            self.MyTable.setItem(count, 3, newItem)
                            result=SnowNLP(comment)
                            sentiment=str(result.sentiments)
                            newItem = QtGui.QTableWidgetItem(sentiment)  
                            self.MyTable.setItem(count, 4, newItem)
                            #sleep(5)
                            
                            ft.write(line+'\n')
                            count+=1
                except:
                    pass
                else:
                    ft.close
            i =i+1
            url="https://m.weibo.cn/api/container/getIndex?type=all&queryVal="+movieName+"&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D"+movieName+"&title="+movieName+"&containerid=100103type%3D1%26q%3D"+movieName+"&page="+str(i)
            data=requests.get(url).json()
            sleep(2)
        newItem = QtGui.QTableWidgetItem("Funished")  
        self.MyTable.setItem(count+1, 0, newItem)
    def restartFunction(self):
        self.MyTable.clear()
        self.MyTable.setHorizontalHeaderLabels(['user','movie','time','comment','sentiment'])
    def setUp(self):
        self.driver = webdriver.Chrome()
    def testEle(self):
        driver = self.driver
        url ="https://www.douban.com/accounts/login"
        driver.get(url)
        #driver.find_element_by_name("form_email").send_keys("zhang.shijie1101@gmail.com")     
        #driver.find_element_by_name("form_password").send_keys("011010642zsj")    
        sleep(25)
        ## Click login  
        driver.find_element_by_name("login").click()  
        sleep(5)
        driver.refresh()
        with open("latestmovie.txt",'r',encoding='utf-8')as f:
            movieitems=f.readlines()
            f.close()
        for item in movieitems:
            movieid=item.split("\t")[0]
            url="https://movie.douban.com/subject/"+str(movieid)+"/comments?status=P"
            driver.get(url)      
            soup = BeautifulSoup(driver.page_source, 'xml')
            while True:
                soup = BeautifulSoup(driver.page_source, 'xml')
                comments=soup.find_all('div',{'class':'comment-item'})
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                for mmid in comments:
                    if(len(mmid.h3.find_all('span',{'class':'comment-info'})[0].find_all('span'))==3):
                        userid=mmid.h3.find_all('span',{'class':'comment-info'})[0].a["href"].split("/")[-2]
                        star=mmid.h3.find_all('span',{'class':'comment-info'})[0].find_all('span')[1]["class"].replace("allstar","").replace("rating","")
                        time=mmid.h3.find_all('span',{'class':'comment-info'})[0].find_all('span')[2]['title']
                        content=mmid.p.get_text().strip().translate(non_bmp_map)
                        print(userid,star,time,content)
                        comment=userid+"\t"+str(movieid)+"\t"+star+"\t"+time+"\t"+content
                        if(len(comment)>5):
                            with open("doubancomments.txt",'at',encoding='utf-8')as ft:
                                ft.write(comment+'\n')
                                ft.close()
                try:
                    elem = driver.find_element_by_partial_link_text('后页')
                    print(driver.current_url)
                    elem.click()
                except:
                    break
                else:
                    driver.refresh()
                    sleep(5)
    def readfile(self):
        with open("latestmovie.txt",'r',encoding='utf-8')as f:
            item=f.readlines()
            f.close()
            return item
    def tearDown(self):
        print('down')
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
        
