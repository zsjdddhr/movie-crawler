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



**************************************************************************************************************************************************************************************************************************************************************************************
WEIBO



**************************************************************************************************************************************************************************************************************************************************************************************







