from selenium import webdriver
from bs4 import BeautifulSoup
import bloompy
import networkx as nx
import matplotlib.pyplot as plt
import pickle as pkl
# 创建有向图
G = nx.DiGraph()
bloom_url = bloompy.ScalableBloomFilter(error_rate=0.001,initial_capacity=10**5)
driver = webdriver.Chrome()
Nankai_cs_url = 'http://cc.nankai.edu.cn'
edges = {}
i = 0
def get_Continue_Url(url):
    if bloom_url.add(url) == True:
        return
    try:
        driver.get(url)
        continue_link = driver.find_element_by_tag_name('a')
        ContinueUrl = driver.find_elements_by_xpath("//a[@href]")
    except:
        return -1
    for elem in ContinueUrl:
        if elem.get_attribute("href") not in edges.setdefault(url,[]):
            if "cc.nankai" in elem.get_attribute("href"):
                if "articleId" not in elem.get_attribute("href"):
                    edges[url].append(elem.get_attribute("href"))
    for elem in edges[url]:
        get_Continue_Url(elem)
def get_Utrl_edge():
    result = []
    for i in range(0,len(edges)):
        for j in edges.keys():
            for url in edges[j]:
                result.append((j,url))
    f = open("pagerank.list","wb+")
    pkl.dump(result,f)
    f.close()
    return result

if __name__ == '__main__':
    f = open("pagerank.list","rb+")
    results = pkl.load(f)
    print("test1")
    for edge in results:
        G.add_edge(edge[0], edge[1])
    pagerank_list = nx.pagerank(G, alpha=0.85)
    print(pagerank_list)
    # nx.draw(G, pos=nx.random_layout(G),node_color = 'b', edge_color = 'r', with_labels = False,font_size = 18, node_size = 20)
    # plt.show()