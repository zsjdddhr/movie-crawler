#coding:utf-8
import unittest
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
from selenium.webdriver.common.keys import Keys  
class seleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    def testEle(self):
        driver = self.driver
        driver.get('https://movie.douban.com/cinema/nowplaying/beijing/')
        #sleep(5)
        #driver.find_element_by_id("login-email").send_keys("18604079328")     
        #driver.find_element_by_id("login-password").send_keys("201100820106zsj")    
        
        ## Click login  
        #driver.find_element_by_name("commit").click()  
        #sleep(30)
        #driver.refresh()
        soup = BeautifulSoup(driver.page_source, 'xml')
        i=0
        showall=driver.find_element_by_class_name('more')
        showall.click()
        internal = soup.find_all(attrs={"data-category":"nowplaying"})
        idlist=[]   
        for mmid in internal:
            detail=""
            movieid=mmid['id']
            title=mmid['data-title']
            score=mmid['data-score']
            star=mmid['data-star']
            date=mmid['data-release']
            duration=mmid['data-duration']
            region=mmid['data-region']
            director=mmid['data-director']
            actors=mmid['data-actors']
            detail=movieid+"\t"+title+"\t"+score+"\t"+star+"\t"+date+"\t"+duration+"\t"+region+"\t"+director+"\t"+actors
            print (detail)
            with open("maoyanid.txt", 'at', encoding='utf-8') as f:
                f.write(detail+'\n')
                f.close
                sleep(1)
    def tearDown(self):
        print('down')

if __name__ == "__main__":
    unittest.main()
