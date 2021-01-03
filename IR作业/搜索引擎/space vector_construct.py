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
    def __init__(self,tf = "",idf = "",all_idf = "",tf_idf = "",tf_title = "",idf_title = "",all_title_idf = "",tf_idf_title = "",total_mum = "",):
        if tf == "":
            self.tf_dic = {}
        if idf == "":
            self.idf_dic = {}
        if all_idf == "":
            self.all_idf = {}
        if tf_idf == "":
            self.tf_idf = {}
        if tf_title == "":
            self.tf_title = {}
        if idf_title == "":
            self.idf_title = {}
        if all_title_idf == "":
            self.all_title_idf = {}
        if tf_idf_title == "":
            self.tf_idf_title = {}
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

    def Count_title(self):
        for home,title,file_name in os.walk("html_file"):
            for i in range(0,len(file_name)):
                file_name[i] = list(jieba.cut(file_name[i][:-4]))
                for word in file_name[i]:
                    print("test")
                    if word == " ":
                        continue
                    # print("test:", word)
                    if word not in self.tf_title.keys():
                        self.tf_title[word] = 1
                    else:
                        self.tf_title[word] = self.tf_title[word] + 1
                    if word not in self.idf_title.keys():
                        self.idf_title[word] = 1
                    else:
                        self.idf_title[word] = self.idf_title[word] + 1
                dic = sorted(self.tf_title.items(), key=lambda tf_title: tf_title[1], reverse=True)
                self.all_title_idf[str(''.join(file_name[i]))] = dic
                f = open("title_tf.dic","wb+")
                pkl.dump(self.all_title_idf,f)
                self.tf_title = {}
                f.close()

    def Count_tf_id(self):
        f = open("tf_alldoc.dic","rb+")
        file = open("idf_alldoc.dic","rb+")
        f_doc = pkl.load(f)
        file_doc = pkl.load(file)
        for i in f_doc.keys():
            self.tf_idf[i] = {}
            doc_len = len(f_doc[i])
            for j in f_doc[i]:
                n = j[1]
                m = file_doc[j[0]]
                # print(n,m)
                # print(n/doc_len * 1/(m/self.total_mum))
                self.tf_idf[i][j[0]] = n/doc_len * 1/(m/self.total_mum)
        file.close()
        f.close()
        f = open("tf_idf.dic","wb+")
        pkl.dump(self.tf_idf,f)
        f.close()
    def get_idf_title(self,doc,key):
        count = 0
        for i in doc.keys():
            for j in doc[i]:
                if j[0] == key:
                    count = count + j[1]
        return count
    def Count_tf_idf_title(self):
        f = open("title_tf.dic","rb+")
        f_doc = pkl.load(f)
        for i in f_doc.keys():
            if i == "":
                continue
            self.tf_idf_title[i] = {}
            doc_len = len(f_doc[i])
            for j in f_doc[i]:
                if j[0] == "-":
                    continue
                n = j[1]
                m = self.get_idf_title(f_doc,j[0])
                self.tf_idf_title[i][j[0]] = (n / doc_len) * (1 / (m / self.total_mum))
        f.close()
        f = open("tf_idf_title.dic","wb+")
        pkl.dump(self.tf_idf_title,f)
        f.close()


if __name__ == '__main__':
    Count = Tool_tf_idf()
    Count.Count_tf_idf_title()