from selenium import webdriver
from bs4 import BeautifulSoup
import bloompy
blom = bloompy.ScalableBloomFilter(error_rate=0.001,initial_capacity=10**5)
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
        self.ContinueUrl = list(set(self.ContinueUrl))
        f = open("docs.txt", "a+")
        for elem in self.ContinueUrl:
            if (blom.add(elem.get_attribute("href"))):
                print(elem.get_attribute("href"))
            else:
                f.write(elem.get_attribute("href") + '\n')
        self.ContinueUrl = []
        f.close()
        f = open("docs.txt","r")
        file = open("test.txt", "a+")
        for lin in f.readlines():
            if "nankai" in lin:
                if "articleId" not in lin:
                    file.write(str(lin) + '\n')
        f.close()
        file.close()

    def get_html_title(self,file):
        return (file[7:-8])

    def get_Continue_urls(self):
        f = open("test.txt")
        file = open("docs.txt", "a+")
        lines = f.readlines()
        i = 0
        print(len(lines))
        for line in lines:
            try:
                driver.get(line)
                i = i + 1
                print(i)
            except:
                continue
            continue_link = driver.find_element_by_tag_name('a')
            self.ContinueUrl = driver.find_elements_by_xpath("//a[@href]")
            self.ContinueUrl = list(set(self.ContinueUrl))
            for elem in self.ContinueUrl:
                if not (blom.add(elem.get_attribute("href"))):
                    file.write(elem.get_attribute("href") + '\n')
            self.ContinueUrl = []
        f.close()
        f = open("docs.txt", "r")
        file = open("test.txt", "w")
        for lin in f.readlines():
            if "cc.nankai" in lin:
                if "articleId" not in lin:
                    file.write(str(lin) + '\n')
        f.close()
        file.close()
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
        i = 0
        print(len(lines))
        for url1 in lines:
            try:
                driver.get(url1)
                i = i + 1
                print(i)
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
        f.close()
        file.close()
    def url_title_map(self,title,map):


if __name__ == '__main__':
    spider = URL_TOOL()
    spider.get_Continue_Url(Nankai_cs_url)
    spider.get_Continue_urls()
    spider.get_UrlPage()

