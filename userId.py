import pandas as pd
import math
import numpy as np
from math import exp
from numpy import linalg as la
import os,time
import re
from snownlp import SnowNLP
def dataprepare(fileName):
    with open(fileName,'r',encoding='utf-8')as f:
        lines = f.readlines()
    f.close()
    i=0
    for line in lines:
        i=i+1
        try:
            yy=line.split('\t')
            if(len(yy)<=3):
                print(str(i)+"\n"+line)
                lines.remove(line)        
        except:
            pass
    with open(fileName,'r+',encoding='utf-8')as f:
        read_dat=f.read()
        f.seek(0)
        f.truncate()
        for i in lines:
            f.write(i)         
    f.close()    
def make_data():
    result={}
    with open('doubancomments.txt','r',encoding='utf-8')as f:
        lines = f.readlines()
        i=0
        for line in lines:
            i=i+1
            if(i<=100000):
                try:
                    line =line.split('\t')
                    userId= line[0]
                    movieId = line[1]
                    score= float(line[2])/10
                    time =line[3]
                    comments=line[4].replace("\n","")
                except:
                    pass
                else:
                    if userId not in result.keys():
                        result[userId]={}
                    result[userId][movieId] ={}
                    result[userId][movieId]["time"]=time
                    result[userId][movieId]["score"]=score
                    result[userId][movieId]["comments"]=comments
                    #print(userId+movieId+str(score))
            else:
                break
    f.close()
    return result

def userId(fileName):
    with open(fileName,'r',encoding='utf-8')as f:
        items = f.readlines()
        userId =set()
        for item in items:
            line = item.split('\t')
            #print(line)
            if(len(line)>=3):
                userId.add(line[0])
        f.close()
    with open("userId.txt",'at',encoding='utf-8')as ft:
        for user in userId:
            ft.write(user+'\n')
            print(user)
        ft.close()
    return userId
def movieId(fileName):
    with open(fileName,'r',encoding='utf-8')as f:
        items = f.readlines()
        userId =set()
        for item in items:
            line = item.split('\t')
            #print(line)
            if(len(line)>=3):
                userId.add(line[1])
        f.close()
    with open("movieId.txt",'at',encoding='utf-8')as ft:
        for user in userId:
            ft.write(user+'\n')
            print(user)
        ft.close()
def similarity(result,per1,per2):
    si={}
    for item in result[per1].keys():
        if item in result[per2].keys():
            #print(item)
            si[item]=1
    if len(si)<2:
        return 0
    per1_rating =[]
    per2_rating =[]
    for i in si:
        #print(i)
        per1_rating.append(result[per1][i]["score"])
        per2_rating.append(result[per2][i]["score"])
        #print(per1_rating,per2_rating)
    d={'per1':per1_rating,'per2':per2_rating}
    df = pd.DataFrame(data=d)
    try:
        result=df['per1'].corr(df['per2'])
    except:
        return 0
    else:
        if math.isnan(result):
            return 0
    return result
"""sample=[]
result=make_data()
for i in result.keys():
	if(len(result[i].values())>5):
		sample.append(i)
for j in range(0, len(sample)):
    for l in range(j+1,len(sample)):
        print(similarity(result,sample[j],sample[l]))
"""

def topMatches(result,person,n):
    score=[(similarity(result,person,other),other) for other in result if other!=person]
    score.sort()
    score.reverse()
    return score[0:n]
"""sample=[]
result=make_data()
for i in result.keys():
	if(len(result[i].values())>10):
		sample.append(i)
for j in sample:
    print(j)
    print(topMatches(result,j,50))
"""
def recommendations_item(results,person,n):
    #results=make_data()
    userid=list(results.keys())
    userid.remove(person)
    totals={}
    counts={}
    for other in userid:
        distance=similarity(results,person,other)
        if distance>0.5:
            for movie in results[other]:
                if movie not in results[person]:
                    totals.setdefault(movie,0)
                    totals[movie]+=distance*results[other][movie]["score"]
                    counts.setdefault(movie,0)
                    counts[movie]+=distance
    rankings=[(totals[movie]/counts[movie],movie)for movie in totals]
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]
"""sample=[]
result=make_data()
for i in result.keys():
	if(len(result[i].values())>10):
		sample.append(i)
for j in sample:
    print(j)
    print(recommendations_item(result,j,10))
"""
def usersData(results):
    movieList={}
    for per in results:
        for movie in results[per]:
            if movie not in movieList:
                movieList[movie]={}
            movieList[movie][per]=results[per][movie]["score"]
            #print(movie,per)
    return movieList
def similarItems(movieData,movie1,movie2):
    si={}
    m1=[]
    m2=[]
    for user in movieData[movie1]:
        if user in movieData[movie2]:
            si[user]=1
    if len(si)==0:
        return 0
    for item in si:
        m1.append(movieData[movie1][item])
        m2.append(movieData[movie2][item])
    d={'m1':m1,'m2':m2}
    df = pd.DataFrame(data=d)
    try:
        result=df['m1'].corr(df['m2'])
    except:
        return 0
    else:
        if math.isnan(result):
            return 0
    return result
def topMatchesMovie(results,movie1,n):
    movieData=usersData(results)
    score=[(similarItems(movieData,movie1,other),other) for other in movieData if other!=movie1]
    score.sort()
    score.reverse()
    return score[0:n]
def movieRecommendations_movie(results,person,n):
    result=usersData(results)
    userRating=results[person]
    unWatch=[]
    scores={}
    counts={}
    for m1 in userRating:
        for (simi,m2) in topMatchesMovie(results,m1,10):
            if m2 not in results[person]:
                #print(m2)
                scores.setdefault(m2,0)
                counts.setdefault(m2,0)
                scores[m2]+=simi*userRating[m1]["score"]
                #print(scores[m2])
                counts[m2]+=simi
                #print(counts[m2])s
    rankings=[(score/counts[item],item) for item,score in scores.items( )]
    rankings.sort()
    rankings.reverse()
    return rankings

def getData(fileName):
     header = ['user_id', 'movie_id', 'rating', 'timestamp','comment']
     df = pd.read_csv(fileName, sep='\t', names=header)
     return df
def userNegativeItem(sample,userId):
    ratedList=list(set(sample[sample['user_id']==userId]['movie_id']))
    unratedList=[i for i in set(sample['movie_id'].values) if i not in ratedList]
    popularity =[len(sample[sample['movie_id']==item]['user_id']) for item in unratedList]
    movies = pd.Series(popularity,index=unratedList)
    movies=movies.sort_values(ascending=False)[:len(ratedList)]
    return list(movies.index)
def userPositiveItem(sample,userId):
    movies=list(set(sample[sample['user_id']==userId]['movie_id']))
    return movies

def initialDict(sample,userId):
    positiveList=userPositiveItem(sample,userId)
    negativeList=userNegativeItem(sample,userId)
    dic={}
    for item in positiveList:
        dic[item]=1
    for item in negativeList:
        dic[item]=0
    return dic

def initialDict2(sample,userId):
    dic={}
    ratedList=list(set(sample[sample['user_id']==userId]['movie_id']))
    for movie in ratedList:
        dic[movie]=float(list(sample[sample.user_id==userId][sample.movie_id==movie]['rating'].values)[0])/10
        #print(dic[movie])
    return dic    
def inimodel(sample,userID):
    inimodel={}
    for user in userID:
        userDict= initialDict(sample,user)
        inimodel[user]=userDict
    return inimodel
        
def iniParaArray(userID,movieID,classCount):
    inip=np.random.rand(len(userID),classCount)
    iniq=np.random.rand(classCount,len(movieID))
    arrayP=pd.DataFrame(inip,columns=range(0,classCount),index=userID)
    arrayq=pd.DataFrame(iniq,columns=movieID,index=range(0,classCount))
    return arrayP,arrayq
def userLists(sample):
    return list(sample.user_id.unique())

def movieLists(sample):
    return list(sample.movie_id.unique())
def sigmod(x):
    return 1.0/(1+exp(-x))
def lfmCaculate(p,q,userId,movieId):
    p=np.mat(p.loc[userId].values)
    q=np.mat(q[movieId].values).T
    r=(p*q).sum()
    r=sigmod(r)
    return r
def lfModel(sample,classCount,counts,alpha,lamda):
    userID=userLists(sample)
    movieID=movieLists(sample)
    p,q=iniParaArray(userID,movieID,classCount)
    iniModel=inimodel(sample,userID)
    for i in range(0,counts):
        for user,userItem in iniModel.items():
            for movie,rui in userItem.items():
                #print(rui)
                eui=rui-lfmCaculate(p,q,user,movie)
                #print(eui)
                for c in range(0, classCount):
                    p[c][user]+=alpha*(eui*q[movie][c]-lamda*p[c][user])
                    q[movie][c]+=alpha*(eui*p[c][user]-lamda*q[movie][c])
                    #print(q[movie][c])
        alpha*=0.9
    return p,q

def recommend(sample,p,q,userId,n):
    userList=userLists(sample)
    movieList=movieLists(sample)
    otherList=[movie for movie in movieList if movie not in userList]
    results=[(lfmCaculate(p,q,userId,movie), movie)for movie in otherList]
    results.sort()
    results.reverse()
    return results[:n]

def sigmaPct(sigma,percentage=0.9):
    sumSigma=sum(sigma**2)
    squaSum=0
    num=0
    for i in sigma:
        squaSum+=i**2
        num+=1
        if squaSum>=sumSigma*percentage:
            return num
        
def createData(sample):
    userID=userLists(sample)
    movieID=movieLists(sample)
    inidata=np.zeros([len(userID),len(movieID)])
    for i in range(0,len(userID)):
        for j in range(0,len(movieID)):
            #print(j)
            ratedList=list(set(sample[sample['user_id']==userID[i]]['movie_id']))
            #print(ratedList)
            if movieID[j] in ratedList:
                #print(userID[i],movieID[j])
                #x=list(sample[sample.user_id==userID[i]][sample.movie_id==movieID[j]]['rating'].values)
                #print(x)                    
                inidata[i][j]=float(list(sample[sample.user_id==userID[i]][sample.movie_id==movieID[j]]['rating'].values)[0])/10            
                print(inidata[i][j])
    arrayP=pd.DataFrame(inidata,columns=movieID,index=userID)
    return arrayP
def checkCh(word):
    zh_pattern=re.compile(u'[\u4e00-\u9fa5]+')
    match=zh_pattern.search(word)
    if word==None:
        return False##no chinese words
    return True##chinese
    
def sentimentAnalysis(fileName):
    #senMonth= time.ctime(os.stat(fileName).st_mtime).split(" ")[1]
    #senDay= time.ctime(os.stat(fileName).st_mtime).split(" ")[2]
    file=fileName.replace(".txt","")
    dic={"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    with open(fileName,'r',encoding='utf-8')as f:
        items = f.readlines()
    f.close()
    for item in items:
        senMonth= time.ctime(os.stat(fileName).st_mtime).split(" ")[1]
        senDay= time.ctime(os.stat(fileName).st_mtime).split(" ")[2]
        senYear="2018"
        try:
            item=item.split("\t")
            user=item[0]
            #print(user)
            times=item[1]
            #print(times)
            comment=item[2]
        except:
            pass
        if checkCh(times):
            if "昨天" in times:
                day=int(senDay)-1
            #print(senMonth)
            senMonth=dic[senMonth]
        try:
            times=times.split("-")
            if len(times)==3:
                senDay=times[2]
                senMonth=times[1]
                senYear=times[0]
        except:
            pass
        result=SnowNLP(comment)
        sentiment=result.sentiments
        line=user+"\t"+file+"\t"+str(senYear)+"\t"+str(senMonth)+"\t"+str(senDay)+"\t"+ str(sentiment)+"\t"+str(sentiment*5)
        with open("sentiment.txt",'at',encoding='utf-8')as ft:
            ft.write(line+"\n")
            #print(line)
        ft.close()
        
    
                
                
            


            
            
    
    
    
                
        
    
    
    
                    
            
            
    








