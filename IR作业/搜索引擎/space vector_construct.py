import nltk
from collections import Counter
import numpy as np
import os
import jieba
import pickle as pkl
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

class Tool_tf_idf:
    def __init__(self,tf = "",idf = "",all_idf = "",tf_idf = "",total_mum = ""):
        if tf == "":
            self.tf_dic = {}
        if idf == "":
            self.idf_dic = {}
        if all_idf == "":
            self.all_idf = {}
        if tf_idf == "":
            self.tf_idf = {}
        if total_mum == "":
            self.total_mum = len(get_files("html_file"))

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

    def Count(self,resfile):
        infile = open(resfile)
        print(resfile)
        f = infile.readlines()
        count = len(f)
        # print(count)
        infile.close()
        s = open(resfile)
        i = 0
        while i < count:
            line = self.seg_sentence(str(' '.join(jieba.cut(s.readline()))))
            # print(line)
            # 去换行符
            line = line.rstrip('\n')
            # print("line",line)
            words = line.split(" ")
            # print("words",words)

            for word in words:
                if word == "":
                    continue
                #print("test:", word)
                if word not in self.tf_dic.keys():
                    self.tf_dic[word] = 1
                else:
                    self.tf_dic[word] = self.tf_dic[word] + 1
                if word not in self.idf_dic.keys():
                    self.idf_dic[word] = 1
                else:
                    self.idf_dic[word] = self.idf_dic[word] + 1
            i = i + 1
        # 字典按键值降序
        dic = sorted(self.tf_dic.items(), key=lambda tf_dic: tf_dic[1], reverse=True)
        self.all_idf[resfile] = dic
        print(self.all_idf)
        s.close()
        self.tf_dic = {}

    def Count_all(self):
        for file_name in get_files("html_file"):
            self.Count(file_name)
        f = open("tf_alldoc.dic","wb+")
        pkl.dump(self.all_idf,f)
        f.close()
        f = open("idf_alldoc.dic","wb+")
        pkl.dump(self.idf_dic,f)
        f.close()

if __name__ == '__main__':
    IDF = Tool_tf_idf()
    IDF.Count_all()