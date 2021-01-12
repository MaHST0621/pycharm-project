import jieba
import math
import pickle as pkl
import operator
import numpy as np
from numpy import nan as NaN
def stopwordslist():
    file_name = "stopwords/cn_stopwords.txt"
    stopwords = [line.strip() for line in open(file_name,encoding='UTF-8').readlines()]
    return stopwords

def seg_sentence(sentence):
    sentence_seged = jieba.cut_for_search(sentence.strip())
    stopwords = stopwordslist()  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

class Searcher:

    def __init__(self,idf = "" ,tf_idf = "",tf_idf_title = "",index = "",wordset = "",title_wordset = "",index_title = "",idf_title = ""):
        if index == "":
            f = open("words_title.index","rb+")
            self.index = pkl.load(f)
            f.close()
        if index_title == "":
            f = open("title_url.index","rb+")
            self.index_title = pkl.load(f)
            f.close()
        if tf_idf == "":
            f = open("tf_idf.dic","rb+")
            self.tf_idf = pkl.load(f)
            f.close()
        if tf_idf_title == "":
            f = open("title_tfidf.dic","rb+")
            self.tf_idf_title = pkl.load(f)
            f.close()
        if wordset == "":
            f = open("wordset.list","rb+")
            self.wordset = pkl.load(f)
            f.close()
        if idf == "":
            f = open("idf.dic","rb+")
            self.idf = pkl.load(f)
            f.close()
        if idf_title == "":
            f = open("idf_title.dic","rb+")
            self.idf_title = pkl.load(f)
            f.close()
        if title_wordset == "":
            f = open("wordset_title.list", "rb+")
            self.wordset_list = pkl.load(f)
            f.close()

    def getCos(self, vec_a, vec_b):  # 求余弦值
        sum = 0
        sq1 = 0
        sq2 = 0
        for i in range(len(vec_a)):
            sum += float(vec_a[i]) * float(vec_b[i])
            sq1 += pow(float(vec_a[i]), 2)
            sq2 += pow(float(vec_b[i]), 2)
        try:
            result = round(float(sum) / (np.sqrt(sq1) * np.sqrt(sq2)), 2)
        except ZeroDivisionError:
            result = 0.0
        return result

    def get_tf_idf(self,query):
        query = seg_sentence(str(' '.join(jieba.cut_for_search(query))).replace(" ",""))
        words = query.split(" ")
        length = len(words) - 1
        query_tf_idf = {}
        query_tf = dict.fromkeys(self.wordset_list,0)
        for i in words:
            try:
                query_tf[i] += 1
            except:
                continue
        tflist = query_tf
        idfs = self.idf_title
        tfidf = {}
        for word,tfval in tflist.items():
            tfidf[word] = tfval * idfs[word]
        query_tf_idf = tfidf
        return query_tf_idf


    def search(self, query):
        # 计算tf-idf,找出候选doc
        re_tf_idf = {}
        query_tfidf = self.get_tf_idf(query)
        for file,word in self.tf_idf_title.items():
            if file == "html_file\.txt":
                continue
            re_tf_idf[file] = self.getCos(list(query_tfidf.values()),list(self.tf_idf_title[file].values()))
        # 排序
        for i in re_tf_idf:
            if math.isnan(re_tf_idf[i]):
               re_tf_idf[i] = 0.0
        result = sorted(re_tf_idf.items(),reverse=True,key=lambda x:x[1])
        result_doc = []
        for i in result:
            if i[1] != 0.0:
                result_doc.append(i[0])
        print(result)
if __name__ == '__main__':
    search = Searcher()
    query = input("请输入：")
    search.search(query)
