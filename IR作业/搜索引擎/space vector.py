import glob
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
from collections import Counter
import numpy as np
import os
from collections import OrderedDict

def get_files(dir, file_type='.txt'):
    file_list = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            if file_type in filename:
                file_list.append(os.path.join(home,filename))
    return file_list

def stopwordslist():
    for file_name in get_files("stopwords"):
        stopwords = [line.strip() for line in open(file_name,encoding='UTF-8').readlines()]
    return stopwords

def give_path(fld_path):                             #give path of the folder containing all documents
    dic = {}
    file_names = get_files(fld_path)
    for file in file_names:
        name = file.split('/')[-1]
        with open(file, 'r', errors='ignore') as f:
            data = f.read()
        dic[name] = data
    return dic

def wordList_removePuncs(doc_dict):
    stop = stopwordslist()
    wordList = []
    for doc in doc_dict.values():
        for word in doc:
            if not word in stop:
                wordList.append(word)
    return wordList
if __name__ == '__main__':
   t = give_path("html_file")
   gg = wordList_removePuncs(t)
   print(gg)