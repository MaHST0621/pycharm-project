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
        f.close()
        f = open("docs.txt","r")
        file = open("test.txt", "w")
        for lin in f.readlines():
            if "cc.nankai" in lin :
                file.write(str(lin) + '\n')

    def get_html_title(self,file):
        return (file[7:-8])

    def remove(self,string):
        string = string.replace(" ","")
        string = string.replace("/","_")
        string = string.replace("【","")
        string = string.replace("】", "")
        string = string.replace("“", "")
        string = string.replace("”", "")
        string = string.replace("\"", "")
        return string

    def get_UrlPage(self):
        f = open("test.txt")
        lines = f.readlines()
        for url1 in lines:
            try:
                driver.get(url1)
            except:
                continue
            html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
            soup = BeautifulSoup(html, 'lxml')
            srtt = self.remove(str(soup.title))
            file = open("html_file/" + self.get_html_title(srtt) + '.txt',"a+")
            try:
                text = driver.find_element_by_class_name('wp_articlecontent').text
                file.write(text)
            except:
                continue

if __name__ == '__main__':
    spider = URL_TOOL()
    pider.get_Continue_Url(Nankai_cs_url)
    spider.get_UrlPage()

