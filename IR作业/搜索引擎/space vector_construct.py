import nltk
from collections import Counter
import numpy as np
import os
import jieba
import pickle as pkl
import math
def get_files(dir, file_type='.txt'):
    file_list = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            if file_type in filename:
                file_list.append(os.path.join(home,filename))
    return file_list

def stopwordslist():
    file_name = get_files("stopwords")[1]
    stopwords = [line.strip() for line in open(file_name,encoding='UTF-8').readlines()]
    return stopwords

def computeTF(wordSet, split):
    tf = dict.fromkeys(wordSet, 0)
    for word in split:
        if word == "":
            continue
        tf[word] += 1
    return tf

def computeIDF(wordset,tfList):
    idfDict = dict.fromkeys(wordset, 0)  # 词为key，初始值为0
    N = len(tfList)  # 总文档数量
    for tf in tfList:  # 遍历字典中每一篇文章
        for word, count in tfList[tf].items():  # 遍历当前文章的每一个词
            if count > 0:  # 当前遍历的词语在当前遍历到的文章中出现
                idfDict[word] += 1  # 包含词项tj的文档的篇数df+1
    for word, Ni in idfDict.items():  # 利用公式将df替换为逆文档频率idf
        idfDict[word] = math.log10(N / Ni)  # N,Ni均不会为0
    return idfDict  # 返回逆文档频率IDF字典

def computeTFIDF(tflist, idfs):  # tf词频,idf逆文档频率
    tfidf = {}
    for tf in tflist:
        tfidf[tf] = {}
        for word, tfval in tflist[tf].items():
            tfidf[tf][word] = tfval * idfs[word]
    return tfidf
class Tool_tf_idf:
    def __init__(self,tf = "",idf = "",tf_idf = "",tf_title = "",idf_title = "",tf_idf_title = "",total_mum = "",wordset = "",wordset_title = ""):
        if tf == "":
            self.tf_dic = {}
        if idf == "":
            self.idf_dic = {}
        if tf_idf == "":
            self.tf_idf = {}
        if wordset == "":
            self.wordset = {}
        if wordset_title == "":
            self.wordset_title = {}
        if tf_title == "":
            self.tf_title = {}
        if idf_title == "":
            self.idf_title = {}
        if tf_idf_title == "":
            self.tf_idf_title = {}

    def seg_sentence(self,sentence):
        sentence_seged = jieba.cut(sentence.strip())
        stopwords = stopwordslist()  # 这里加载停用词的路径
        outstr = ''
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr
    def get_wordset(self):
        file_term_list = []
        file_term_dic = []
        result_list = 0
        file_name = get_files("html_file")
        for file in file_name:
            s = open(file,"r")
            line = self.seg_sentence(str(' '.join(jieba.cut(s.readline()))))
            line = line.rstrip('\n')
            words = line.split(" ")
            for word in words:
                if word == "":
                    continue
                file_term_list.append(word)
            result_list = len(file_term_list) + result_list
            if file_term_dic == []:
                file_term_dic = file_term_list
            else:
                file_term_dic.extend(file_term_list)
            file_term_list = []
        self.wordset = set(file_term_dic)
        # print(result_list)
        # print(len(file_term_dic))
        # print(file_term_dic)
        # print(len(set(file_term_dic)))
        #print(self.wordset)
        pkl.dump(self.wordset,open("wordset.list","wb+"))

    def Count_tf(self):
        self.get_wordset()
        docs = get_files("html_file")
        for file in docs:
            s = open(file)
            line = self.seg_sentence(str(' '.join(jieba.cut(s.readline()))))
            line = line.rstrip('\n')
            words = line.split(" ")
            self.tf_dic[file] = computeTF(self.wordset,words)
            s.close()
        # pkl.dump(self.tf_dic,open("tf.dic","wb+"))

    def Count_idf(self):
        self.Count_tf()
        tflist = self.tf_dic
        self.idf_dic = computeIDF(self.wordset,tflist)
        pkl.dump(self.idf_dic,open("idf.dic","wb+"))


    def Count_tfidf(self):
        self.Count_idf()
        tf = self.tf_dic
        idf = self.idf_dic
        self.tf_idf = computeTFIDF(tf,idf)
        print(self.tf_idf)
        pkl.dump(self.tf_idf,open("tf_idf.dic","wb+"))

    def get_title_wordset(self):
        docs = get_files("html_file")
        file_term_dic = []
        file_term_list = []
        for file in docs:
            s = file[10:-4]
            line = self.seg_sentence(str(' '.join(jieba.cut(s))))
            line = line.rstrip('\n')
            words = line.split(" ")
            for word in words:
                if word == "":
                    continue
                file_term_list.append(word)
            if file_term_dic == []:
                file_term_dic = file_term_list
            else:
                file_term_dic.extend(file_term_list)
            file_term_list = []
        self.wordset_title = set(file_term_dic)
        pkl.dump(self.wordset_title, open("wordset_title.list", "wb+"))

    def Count_title_tf(self):
        self.get_title_wordset()
        docs = get_files("html_file")
        for file_name in docs:
            tf = dict.fromkeys(self.wordset_title, 0)
            title = file_name[10:-4]
            line = self.seg_sentence(str(' '.join(jieba.cut(title))))
            line = line.rstrip('\n')
            words = line.split(" ")
            dic = {}
            for word in words:
                if word == "":
                    continue
                tf[word] += 1
            self.tf_title[file_name] = tf
        return self.tf_title

    def Count_title_idf(self):
        tfList = self.Count_title_tf()
        idfDict = dict.fromkeys(self.wordset_title, 0)  # 词为key，初始值为0
        print(self.wordset_title)
        print(idfDict)
        if "幸运" in idfDict.keys():
            print("yes,init")
        N = len(tfList)  # 总文档数量
        for tf in tfList:  # 遍历字典中每一篇文章
            for word, count in tfList[tf].items():  # 遍历当前文章的每一个词
                if count > 0:  # 当前遍历的词语在当前遍历到的文章中出现
                    idfDict[word] += 1  # 包含词项tj的文档的篇数df+1
        print(idfDict)
        if "幸运" in idfDict.keys():
            print("yes,df")
        for word, Ni in idfDict.items():  # 利用公式将df替换为逆文档频率idf
            idfDict[word] = math.log10(N / Ni)  # N,Ni均不会为0
        print(idfDict)
        if "幸运" in idfDict.keys():
            print("yes,idf")
        self.idf_title = idfDict
        pkl.dump(self.idf_title,open("idf_title.dic","wb+"))
        return self.idf_title  # 返回逆文档频率IDF字典

    def Count_title_tfidf(self):
        self.Count_title_idf()
        tfidf = {}
        tflist = self.tf_title
        idfs = self.idf_title
        if "幸运" in self.idf_title.keys():
            print("yes")
        print(self.wordset_title)
        for tf in tflist:
            tfidf[tf] = {}
            for word, tfval in tflist[tf].items():
                tfidf[tf][word] = tfval * idfs[word]
        self.tf_idf_title = tfidf
        pkl.dump(self.tf_idf_title,open("title_tfidf.dic","wb+"))
        return tfidf
if __name__ == '__main__':
    Count = Tool_tf_idf()
    Count.Count_tfidf()
    Count.Count_title_tfidf()