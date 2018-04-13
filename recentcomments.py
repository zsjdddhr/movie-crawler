#coding:utf-8
import unittest
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
import sys
from selenium.webdriver.common.keys import Keys  
class seleniumTest(unittest.TestCase):
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
        with open("new.txt",'r',encoding='utf-8')as f:
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
        with open("new.txt",'r',encoding='utf-8')as f:
            item=f.readlines()
            f.close()
            return item
    def tearDown(self):
        print('down')

if __name__ == "__main__":
    unittest.main()

