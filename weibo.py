import requests
import json
from time import sleep
import sys
import re
class WeiboCollection:
    def __init__(self, file):
        self.file = file
    def readFile(self, file):
        with open(file,'r',encoding='utf-8')as f:
            item = f.readlines()
            f.close
        return item
    def deletRepetedItems(self,items):
        movieItems=[]
        for i in items:
            if i not in movieItems:
                movieItems.append(i)
        return movieItems
    def intoFile(self,lists,fileName):
        with open(fileName, 'at', encoding='utf-8') as ft:
            for item in lists:
                ft.write(item)
                ft.close
    def catchBlogs(self, movieName, movieid):
        i=2
        wrong=requests.get('https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%E7%BE%9E%E7%BE%9E%E7%9A%84%E9%93%81%E6%8B%B3&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%BE%9E%E7%BE%9E%E7%9A%84%E9%93%81%E6%8B%B3&title=%E7%BE%9E%E7%BE%9E%E7%9A%84%E9%93%81%E6%8B%B3&containerid=100103type%3D1%26q%3D%E7%BE%9E%E7%BE%9E%E7%9A%84%E9%93%81%E6%8B%B3&page=50').json()
        url="https://m.weibo.cn/api/container/getIndex?type=all&queryVal="+movieName+"&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D"+movieName+"&title="+movieName+"&containerid=100103type%3D1%26q%3D"+movieName+"&page="+str(i)
        data=requests.get(url).json()
        while data["ok"]==1:
            url="https://m.weibo.cn/api/container/getIndex?type=all&queryVal="+movieName+"&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D"+movieName+"&title="+movieName+"&containerid=100103type%3D1%26q%3D"+movieName+"&page="+str(i)
            data=requests.get(url).json()
            with open(str(movieid)+".txt",'at',encoding='utf-8')as ft:
                try:
                    js = data["data"]["cards"][0]["card_group"]
                    for jss in js:
                        Pattern=re.compile(u"<(.*)>")
                        line=''
                        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                        text=jss['mblog']['text'].translate(non_bmp_map)
                        if(len(Pattern.sub(r'',text))>=3):
                            line= str(jss['mblog']['id'])+'\t'+str(jss['mblog']['created_at'])+'\t'+str(Pattern.sub(r'',text))
                            print(line)
                            ft.write(line+'\n')
                except:
                    break
                else:
                    ft.close
            i =i+1
            url="https://m.weibo.cn/api/container/getIndex?type=all&queryVal="+movieName+"&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D"+movieName+"&title="+movieName+"&containerid=100103type%3D1%26q%3D"+movieName+"&page="+str(i)
            data=requests.get(url).json()
            sleep(2)
        return("finished!")
    def findMovie(self):
        items = []
        with open("maoyanid3.txt",'r',encoding='utf-8')as f:
            item = f.readlines()
            for i in item:
                line=i.split("  ")
                movie = line[1]
                items.append(movie)
            f.close
        with open("maoyanid3.txt",'at',encoding='utf-8')as ft:
            for t in items:
                ft.write(t+'\n')
            ft.close
    def blogs(self):
         items = []
         with open("maoyanid3.txt",'r',encoding='utf-8')as f:
             item = f.readlines()
             #print(item)
             for i in item:
                 line=i.split("\t")
                 movie = line[1].replace(" ","")
                 movieid=line[0].replace(" ","")
                 print(movie,movieid)
                 self.catchBlogs(movie,movieid)


wei = WeiboCollection("maoyanid3.txt")
wei.blogs()


    
        
        
    
