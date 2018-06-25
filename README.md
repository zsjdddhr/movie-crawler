# movie-crawler
collect movie infor from douban.com and maoyan.com// collect blogs from m.weibo.com
all the collected data will be used as data analysis and recommendation algorithm research

**************************************************************************************************************************************************************************************************************************************************************************************
MAOYAN
This one is quite simple because we can use the public API to download the raw jason file.
in this part, we need to acquire the technology of python, request and beautifulsoup.

****
how to install request and Beautifulsoup
simply use cmd line as follows:
pip install requests 
pip install BeautifulSoup4

****

how to get the public Api from Maoyan.
the first funny thing is that you cannot load more user comments under each movie page.
so we need to search m.maoyan.com e.g. https://m.maoyan.com/movie/341138?_v_=yes
1. F12
2. choose NETWORK in the tool bar
3. choose XHR in the second function bar
4. push see more movie comments in the page.
then you can get an url like that:
https://m.maoyan.com/mmdb/comments/movie/341138.json?_v_=yes&offset=0&startTime=0
when the page load data using ajax, the web server will receive the data from those websites.
u just need to do is replace the movie id and offset=0,20,40,60...
i think we don't need any other advanced technology, then we can get the whole data from maoyan.
but data will be expired in one month or...
we cannot collect the data commented last year.

**************************************************************************************************************************************************************************************************************************************************************************************

DOUBAN
I mainly use selenium to collect the user rating behaviors from douban website.
1. use all.py to collect the movie information including name, genre, actors and etc. Then save the data into 
onlycompletefinal.txt
2. use recentcomments.py to collect the user behaviours.
url="https://movie.douban.com/subject/"+str(movieid)+"/comments?status=P"
delete the useless html attributr.
 non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                         
3. split the timestamp to year, month and day, which can be easier to search the records based on time.

**************************************************************************************************************************************************************************************************************************************************************************************
WEIBO
In this part, I mainly collect the blogs under the specific movie title in https://m.weibo.cn using the same method as maoyan to find the json address. The address as follows:
https://m.weibo.cn/api/container/getIndex?type=all&queryVal="+movieName+"&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D"+movieName+"&title="+movieName+"&containerid=100103type%3D1%26q%3D"+movieName+"&page="+str(i) where i represents the number of index.

Pattern=re.compile(u"<(.*)>")
                        line=''
                        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                        text=jss['mblog']['text'].translate(non_bmp_map)
                        if(len(Pattern.sub(r'',text))>=3):
                            line= str(jss['mblog']['id'])+'\t'+str(jss['mblog']['created_at'])+'\t'+str(Pattern.sub(r'',text))
There are lots of emoji in blogs which cannot be controled in python. In that case, I deleted directloy those emoji in the data preparation process using the below codes. 
**************************************************************************************************************************************************************************************************************************************************************************************







