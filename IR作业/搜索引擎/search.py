import jieba
import math
import pickle as pkl
import operator
import numpy as np

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

    def __init__(self, tf_idf = "",tf_idf_title = "",index = "",idf = "",index_title = ""):
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
            f = open("tf_idf_title.dic","rb+")
            self.tf_idf_title = pkl.load(f)
            f.close()
        if tf_idf == "":
            f = open("idf_alldoc.dic","rb+")
            self.idf = pkl.load(f)
            f.close()

    def getCos(self, vec_c, vec_d):  # 求余弦值
        sum = 0
        sq1 = 0
        sq2 = 0
        vec_a = []
        vec_b = []
        for j in vec_c.values():
            vec_a.append(j)
        for j in vec_d.values():
            vec_b.append(j)
        if len(vec_a) < len(vec_b):
            vec_a += [0 for i in range(len(vec_b) - len(vec_a))]
        else:
            vec_b += [0 for i in range(len(vec_a) - len(vec_b))]
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
        for i in words:
            if i == " ":
                continue
            if i in self.idf.keys():
                m = self.idf[i]
            else:
                m = 1
            N = length
            M = len(self.idf.keys())
            n = words.count(i)
            query_tf_idf[i] = n/N * 1/(m/M)
        return query_tf_idf


    def search(self, query):
        # 计算tf-idf,找出候选doc
        re_tf_idf = {}
        for i,j in self.tf_idf.items():
            if i == "html_file\.txt":
                continue
            if i in re_tf_idf:
                re_tf_idf[i] += self.getCos(self.get_tf_idf(query),self.tf_idf[i])
            else:
                re_tf_idf[i]  = self.getCos(self.get_tf_idf(query), self.tf_idf[i])
        # 排序
        sorted_doc = sorted(re_tf_idf.items(), key=operator.itemgetter(0), reverse=True)

        print(sorted_doc)


if __name__ == '__main__':
    search = Searcher()
    query = input("请输入：")
    search.search(query)
