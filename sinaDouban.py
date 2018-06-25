import pandas as pd
import math
import numpy as np
from math import exp
from numpy import linalg as la
import os,time
import re
from snownlp import SnowNLP
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
import requests
import json
from time import sleep
def readFile(fileName):
    with open(fileName,'r',encoding='utf-8')as f:
        items = f.readlines()
    f.close()
    return items
def doubanPrep(fileName):
    header = ['user_id', 'movie_id', 'rating', 'year','month','day','comment']
    df = pd.read_csv(fileName, sep='\t', names=header)
    return df
def sinaPrep(fileName):
    header = ['user_id', 'movie_id', 'year', 'month','day','rating','norRating']
    df = pd.read_csv(fileName, sep='\t', names=header)
    return df
def ratings():
    list(sample[sample.user_id==userId][sample.movie_id==movie]['rating'].values)[0]
def sigmod(x):
    return 1.0/(1+exp(-x))

def dataPre(fileName):
    lists=readFile(fileName)
    for i in lists:
        i=i.split("\t")
        userId=i[0]
        print(userId)
        movieId=i[1]
        rating=i[2]
        time=i[3].split(" ")[0].split("-")
        year=time[0]
        day=time[2]
        month=time[1]
        comment=i[4]
        line=userId+"\t"+movieId+"\t"+str(rating)+"\t"+year+"\t"+month+"\t"+day+"\t"+comment
        writeFile("doubanzhanlang.txt",line)  
def writeFile(fileName,line):
    with open(fileName,'at',encoding='utf-8')as ft:
        ft.write(line)
        #print(user)
    ft.close()
def userNumber(sample):
    return sample.user_id.unique().shape()[0]
def userRating(douban,movieId,year,month,day):
    return list(douban[douban.movie_id==movieId][douban.year==year][douban.month==month][douban.day==day]["rating"].values)
def aveMonth(douban,movieid,year,month):
    sumRatings=0
    ratings=list(douban[douban.movie_id==movieid][douban.year==year][douban.month==month]["rating"].values)
    for i in ratings:
        sumRatings+=sigmod(int(i)/10)
    if len(ratings)==0:
        return 0
    #print(sumRatings)
    #print(len(ratings))
    return sumRatings/len(ratings)
"""
ave=[]
num=[]
for i in date:
    for j in day:
	    if aveDay(30145577,2018,i,j)>0:
		    ave.append(aveDay(30145577,2018,i,j))
		    num.append(str(i)+str(j))
f1 = plt.figure(1)
plt.subplot(211)
ave=np.array(ave)
num=np.array(num)
plt.scatter(num,ave)
plt.show()
"""
def aveDay(douban,movieid,year,month,day):
    sumRatings=0
    ratings=list(douban[douban.movie_id==movieid][douban.year==year][douban.month==month][douban.day==day]["rating"].values)
    for i in ratings:
        sumRatings+=int(i)/10
    if len(ratings)==0:
        return 0,0
    #print(sumRatings)
    #print(len(ratings))
    return sumRatings/len(ratings), len(ratings)

def aveWeibo(weibo,movieid,year,month,day):
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

douban=doubanPrep("doubancommentnew.txt")
weibo=sinaPrep("sentiment.txt")
def plotMovie(douban,weibo,movieid,year):  
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
    rate0, lenth0=aveDay(douban,movieid,year,1,1)
    ave1.append(rate0)
    nnum1.append(lenth0)
    #num1.append("11")
    rate1, lenth1=aveDay(weibo,movieid,year,1,1)
    ave2.append(rate1)
    nnum2.append(lenth1)
    #num2.append("11")
    for i in date:
        for j in day:
            rates, lenth=aveDay(douban,movieid,year,i,j)
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
            rates, lenth=aveWeibo(weibo,movieid,year,ii,jj)
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
    new1=[]
    new2=[]
    for i in range(1,len(ave1)):
        new1.append(ave1[i]-ave1[i-1])
    for j in range(1,len(ave2)):
        new2.append(ave2[j]-ave2[j-1])
   
    #print(len(ave1),len(ave2))                   
    f1 = plt.figure(1)
    plt.subplot(211)
    new1=np.array(new1)
    num1=np.array(list(range(0,count)))
    new2=np.array(new2)
    num2=np.array(list(range(0,count2)))
    #plt.scatter(num1,ave1,marker='x',color='m')
    plot1 = plt.plot(num1,ave1, 'o-',label='Douban values')
    plot2 = plt.plot(num2,ave2, 'r-',label='Weibo values')
    plt.legend()
    #plt.axis([0,361,2,5])
    #plt.scatter(num2,ave2,marker='o',color='r')
    plt.show()
def doubanAveg(douban,movieid):
    ratings=list(douban[douban.movie_id==movieid]["rating"].values)
    sumRatings=0
    for rating in ratings:
        sumRatings+=float(rating/10)
    if len(ratings)==0:
        return 0
    return sumRatings/len(ratings)
def doubanAvegLen(douban,movieid):
    ratings=list(douban[douban.movie_id==movieid]["rating"].values)
    return len(ratings)
def weiboAveg(weibo,movieid):
    ratings=list(weibo[weibo.movie_id==movieid]["rating"].values)
    sumRatings=0
    for rating in ratings:
        sumRatings+=float(rating)
    return sumRatings/len(ratings)
"""
douban and weibo
"""
def weiboDouban(douban,weibo):
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
        d=doubanAveg(douban,i)
        #print(d)
        w=weiboAveg(weibo,i)
       # print(w)
        if w>0.5:
            x.append(d)
            y.append(w*25/3-10/3)
    f1 = plt.figure(1)
    plt.subplot(211)
    x=np.array(x)
    #print(x)
    y=np.array(y)
    #print(y)
    sample=np.linspace(0,5,1000)
    sampley=[i+0.5 for i in sample]
    plt.scatter(x,y,marker='o',color='m')
    #plot1=plt.plot(x,y, 'r',label='polyfit values')
    plot2=plt.plot(sample,sample,'r',label='polyfit values')
    plt.axis([0,5,0,5])
    plt.show()
"""http://api.douban.com/v2/movie/subject/1764796"""
def getMovieInfor(fileName):
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
"""
f1 = np.polyfit(x, y, 3)  
p1 = np.poly1d(f1)  
print(p1)  
  
#也可使用yvals=np.polyval(f1, x)  
yvals = p1(x)  #拟合y值  
  
#绘图  
plot1 = plt.plot(x, y, 's',label='original values')  
plot2 = plt.plot(x, yvals, 'r',label='polyfit values')  
plt.xlabel('x')  
plt.ylabel('y')  
plt.legend(loc=4) #指定legend的位置右下角  
plt.title('polyfitting')  
plt.show()
"""
"""
def func(x, a, b):  
    return a*np.exp(b/x) 
popt, pcov = curve_fit(func, x, y)  
#获取popt里面是拟合系数  
a = popt[0]   
b = popt[1]  
yvals = func(x,a,b) #拟合y值
plot1 = plt.plot(x, y, 's',label='original values')  
plot2 = plt.plot(x, yvals, 'r',label='polyfit values')  
plt.xlabel('x')  
plt.ylabel('y')  
plt.legend(loc=4) #指定legend的位置右下角  
plt.title('curve_fit')  
plt.show() 
def func(x, a, b):  
    return a*pow(x,b)
popt, pcov = curve_fit(func, x, y)  
#获取popt里面是拟合系数  
a = popt[0]   
b = popt[1]  
yvals = func(x,a,b) #拟合y值   
plot1 = plt.plot(x, y, 's',label='original values')  
plot2 = plt.plot(x, yvals, 'r',label='polyfit values')  
plt.xlabel('x')  
plt.ylabel('y')  
plt.legend(loc=4) #指定legend的位置右下角  
plt.title('curve_fit')  
#plt.savefig('test3.png')  
plt.show()  
"""
#douban=doubanPrep("doubancommentnew.txt")
#weibo=sinaPrep("sentiment.txt")
def moviePre(douban,weibo,movieid,year):
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
def negativeWeibo(weibo):
    movieWeibo=list(weibo.movie_id.unique())
    negativeList=[]
    for movie in movieWeibo:
        sentiment=weiboAveg(weibo,movie)
        if sentiment<0.6:
            negativeList.append((sentiment,movie))
    return negativeList
def negativeDouban(weibo,douban):
    negativeList=negativeWeibo(weibo)
    negativeDouban=[]
    for i,j in negativeList:
        result=doubanAveg(douban,j)
        negativeDouban.append((result,doubanAvegLen(douban,j)))
    return negativeDouban
def aveDoubanRating(douban):
    movieDouban=list(douban.movie_id.unique())
    sumRating=0
    for i in movieDouban:
        sumRating+=doubanAveg(douban,i)
    return sumRating/len(movieDouban)
def ratingCount(douban,movieid):
    ratings=list(douban[douban.movie_id==movieid]["rating"].values)
    return len(ratings)
def aveRatingCount(douban):
    movieDouban=list(douban.movie_id.unique())
    sumCount=0
    for i in movieDouban:
        sumCount+=ratingCount(douban,i)
    return sumCount/len(movieDouban)
"""
sentiment vs count
"""
def plotNegativeDouban(weibo,douban):
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
