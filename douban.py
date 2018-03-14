import requests
import json
from time import sleep
filename = ["xinlizui","jiaozhuzhuan","xiadiao","yitian","theater"]
i = 0
while True:
    solditems = [requests.get('http://m.maoyan.com/comments.json?movieid=342381&limit=60&offset=60').json(),
                 requests.get('http://m.maoyan.com/comments.json?movieid=245938&limit=60&offset=60').json(),
                 requests.get('http://m.maoyan.com/comments.json?movieid=1183619&limit=60&offset=60').json(),
                 requests.get('http://m.maoyan.com/comments.json?movieid=344081&limit=60&offset=60').json(),
                 requests.get('http://api.douban.com/v2/movie/in_theaters').json()]
    for j in range(0,5):
        with open(filename[j]+str(i)+".json", 'w') as f:
            #jsondata= json.dumps(data, ensure_ascii = False, indent = 4 )
            json.dump(solditems[j], f)
    i=i+1
    sleep(3600)
