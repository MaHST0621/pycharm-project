#  建索引
from docx import Document as Doc
import jieba
import math
import os
import pickle as pkl
import jieba.analyse as analyse

def get_files(dir, file_type='.txt'):
    file_list = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            if file_type in filename:
                file_list.append(os.path.join(home,filename))
    print(file_list)
    return file_list

def get_TOP_words(file_name):
    try:
        file = open(file_name,"r").read()
    except:
        return -1
    words = analyse.extract_tags(file,5,allowPOS=('n'))   #提取文档中的Top5名词
    return words

def build_index(file_path):
    file_names = get_files(file_path)
    result_dict = {}
    for file_name in file_names:
        words = get_TOP_words(file_name)
        if words == -1:
            continue
        for word in words:
            result_dict.setdefault(word,[])
            result_dict[word].append(file_name[10:-4])
    file = open("words_title.index","wb")
    pkl.dump(result_dict,file)
    file.close()
if __name__ == '__main__':
    build_index("html_file")