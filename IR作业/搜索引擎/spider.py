from selenium import webdriver
from bs4 import BeautifulSoup
# 睡眠时间
import time
import re
import os
import requests
Nankai_cs_url = 'http://cc.nankai.edu.cn'
driver = webdriver.Chrome()
def s(int):
    time.sleep(int)

class URL_TOOL:
    def __init__(self,continue_url = '',):
        if continue_url == '':
            self.ContinueUrl = [];

    def get_Continue_Url(self,url):
        driver.get(url)
        continue_link = driver.find_element_by_tag_name('a')
        self.ContinueUrl = driver.find_elements_by_xpath("//a[@href]")
        f = open("docs.txt", "w")
        for elem in self.ContinueUrl:
            f.write(elem.get_attribute("href") + '\n')

    def get_html_title(self,file):
        return (file[7:-8])
    def get_UrlPage(self):
        f = open("docs.txt")
        lines = f.readlines()
        for url1 in lines:
            if(url1[0] == "j"):
                continue
            try:
                driver.get(url1)
            except:
                continue
            html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
            soup = BeautifulSoup(html, 'lxml')
            self.get_html_title(str(soup.title))
            srtt = str(soup.title).replace('/','_')
            file = open("html_file/" + self.get_html_title(srtt) + '.txt',"w")
            file

if __name__ == '__main__':
    spider = URL_TOOL()
    # spider.get_Continue_Url(Nankai_cs_url)
    spider.get_UrlPage()

