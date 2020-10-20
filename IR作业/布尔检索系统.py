import re
import os
import nltk
import numpy as np
from string import punctuation
from nltk.corpus import stopwords
from collections import defaultdict
sw = stopwords.words('english')
#对文本进行分词
#使用了NLTK工具
def get_words(text):
    #text = re.sub(r"[{}]+".format(punctuation), " ", text)  # 将标点符号转化为空格
    text = text.lower()  # 全部字符转为小写
    words = nltk.word_tokenize(text)  # 分词
    #words = list(set(words).difference(set(sw)))  # 去停用词
    return words
#获取文本文件¶
#给定文本文件目录，获取目录下所有符合要求的文件列表
def get_files(dir, file_type='.txt'):
    file_list = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            if file_type in filename:
                file_list.append(os.path.join(home, filename))
    return file_list
#词法分析¶
#通过正则表达式对查询进行词法分析
# 构造每种类型词的正则表达式，()代表分组，?P<NAME>为组命名
token_or = r'(?P<OR>\|\|)'
token_not = r'(?P<NOT>\!)'
token_word = r'(?P<WORD>[a-zA-Z]+)'
token_and = r'(?P<AND>&&)'
token_lp = r'(?P<LP>\()'
token_rp = r'(?P<RP>\))'
token_yy = r'(?P<YY>\")'
token_dd = r'(?P<DD>\,)'
token_di = r'(?P<DI>\.)'
token_hh = r'(?P<HH>\-)'
lexer = re.compile('|'.join([token_or, token_not, token_word,
                            token_and, token_lp, token_rp,token_yy,token_dd,token_di,token_hh]))  # 编译正则表达式
# 用编译好的正则表达式进行词法分析
def get_tokens(query):
    tokens = []  # tokens中的元素类型为(token, token类型)
    for token in re.finditer(lexer, query):
        tokens.append((token.group(), token.lastgroup))
    print(tokens)
    return tokens
#创建一个字典类型记录符号权重
token_powr = {'WORD':0,'NOT':3,'AND':2,'OR':1,'YY':0,'DD':0,'DI':0,'HH':0}


class BoolRetrieval:
    """
    布尔检索类
    index为字典类型，其键为单词，值为文件ID列表，如{"word": [1, 2, 9], ...}
    """
#sssssssss
    def __init__(self, index_path='',index_double_path='',index_k_path=''):
        if index_path == '':
            self.index = {}
        else:
            data = np.load(index_path, allow_pickle=True)
            self.files = data['files'][()]
            self.index = data['index'][()]

        if index_double_path == '':
            self.index_double = {}
        else:
            data = np.load(index_double_path, allow_pickle=True)
            self.index_double = data['index_double'][()]

        if index_k_path == '':
            self.index_k = {}
        else:
            data = np.load(index_k_path, allow_pickle=True)
            self.index_k = data['index_k'][()]

        self.query_tokens = []
        print(self.query_tokens)

    def build_index(self, text_dir):
        self.files = get_files(text_dir)  # 获取所有文件名
        for num in range(0, len(self.files)):
            f = open(self.files[num])
            text = f.read()
            words = get_words(text)  # 分词
            # 构建倒排索引
            count = 0
            list_1 = []
            #通过dict.setdefault(key,value)函数来构造双字典加列表嵌套模型
            for word in words:
                self.index.setdefault(word,{})
                self.index[word].setdefault(num,[])
                self.index[word][num].append(count)
                count = count +1
            for word in range(0,len(words)-1):
                list_1.append((words[word],words[word+1]))
            for word in range(0,len(list_1)):
                d = ' '.join(list_1[word])
                self.index_double.setdefault(d,{})
                self.index_double[d].setdefault(num,[])
                self.index_double[d][num].append(word)
            for word in words:
                self.index_k_punch(word)
        # print(self.index_double)
        # print(self.files, self.index)
        # print(self.index)
        print(self.index_k)
        np.savez('index_k.npz', index_k=self.index_k)
        np.savez('index_double.npz',index_double = self.index_double)
        np.savez('index.npz', files=self.files, index=self.index)

    def index_k_punch(self,word):
        if len(word) >= 2:
            w = '$' + word +'$'
            for i in range(0,len(w)-1):
                word_k = w[i:i+2]
                self.index_k.setdefault(word_k,[])
                self.index_k[word_k].append(word)
                self.index_k[word_k] = list(set(self.index_k[word_k]))
            for i in range(0,len(w)-2):
                word_k = w[i:i+3]
                self.index_k.setdefault(word_k,[])
                self.index_k[word_k].append(word)
                self.index_k[word_k] = list(set(self.index_k[word_k]))


    def k_punch(self,word):
        result = []
        if len(word) >= 2:
            word = '$' + word +'$'
            for i in range(0,len(word)-1):
                word_k = word[i:i+2]
                result.append(word_k)
            for i in range(0,len(word)-2):
                word_k = word[i:i+3]
                result.append(word_k)
        return list(set(result))

    def jacarrd_k(self,token,list):
        result = {}
        list_1 = []
        for i in range(0,len(list)):
            if abs(len(list[i])-len(token)) < 3:
                list_1.append(list[i])
        list = list_1
        for i in range(0,len(list)):
            a = self.k_punch(list[i])
            b = self.k_punch(token)
            tmp = [c for c in a if c in b]
            tmp_j = len(tmp)/(len(a)+len(b)-len(tmp))
            result.setdefault(list[i],tmp_j)
        result_0 = []
        result = sorted(result.items(), key = lambda kc:kc[1],reverse=True)
        for i in range(0,len(result[:3])):
            result_0.append(result[i][0])
        return result_0
    def pc_soundex(self,query):
        #print('i am colled')
        result = self.k_punch(query)
        result_k = []
        print(result)
        for i in range (0,len(result)):
            result_k.append(self.index_k.get(result[i],[]))
        result_k = sum(result_k,[])
        result_k = list(set(result_k))
        d = []
        for i in self.jacarrd_k(query,result_k):
            d.append(self.make_soundex(i))
        return d
    def make_soundex(self,token_k):
        token = []
        token_k = list(token_k)
        for i in range(0, len(token_k)):
            if token_k[i] != token_k[i - 1]:
                token.append(token_k[i])
        for i in range(1, len(token)):
            if token[i] in ['a', 'e', 'i', 'o', 'u', 'h', 'w', 'y']:
                token[i] = '0'
            elif token[i] in ['b', 'f', 'p', 'v']:
                token[i] = '1'
            elif token[i] in ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z']:
                token[i] = '2'
            elif token[i] in ['d', 't']:
                token[i] = '3'
            elif token[i] in ['l']:
                token[i] = '4'
            elif token[i] in ['m', 'n']:
                token[i] = '5'
            elif token[i] in ['r']:
                token[i] = '6'
        result = []
        for i in range(0, len(token)):
            if token[i] != '0':
                result.append(token[i])
        while (len(result) < 4):
            result.append('0')
        result = ''.join(result[:4])
        return result
    def search(self, query):
        self.query_tokens = get_tokens(query)  # 获取查询的tokens
        #print(self.query_tokens)
        result = []
        # 将查询得到的文件ID转换成文件名
        for num in self.evaluate(0, len(self.query_tokens) - 1):
            result.append(self.files[num])
        if result == []:
            list1 = self.pc_soundex(self.query_tokens[0][0])
            print('搜索的token不存在,您要搜索的或许是这些：', list1)
        return result

    # def phrase_dict_retr(self, biword, dict):
    #     if biword not in self.

    def phrase_search(self,p,q):
        #self.query_tokens = get_tokens(query)
        result_4 = []
        result = []
        result_2 = []
        result_0 = []
        result_1 = set()
        while(p!=q):
            result_4.append((self.query_tokens[p][0],self.query_tokens[p+1][0]))
            p = p+1
        for num in range(0,len(result_4)):
            b = ' '.join(result_4[num])
            result_0.append(b)
        for num in result_0:
            # result3 = set(self.index_double[num])
            result3 = set(self.index_double.get(num,[]))
            result_2.append(result3)
        d = result_2[0]
        for i in range(1,len(result_2)):
            d = d&result_2[i]
            if len(d) == 0:
                return []
        # print(d)
        # print(result_0)
        for t in d:
            value = self.index_double[result_0[0]][t]
            for i in range (1,len(result_0)):
                k = self.index_double[result_0[i]][t]
                value = (i + 1 for i in value)
                value = list(set(k) & set(value))
            if len(value) != 0:
                result.append(t)
        return result
    # 递归解析布尔表达式，p、q为子表达式左右边界的下标
    def evaluate(self, p, q):
        # 解析错误
        if p > q:
            return []
        # 单个token，一定为查询词
        elif p == q:
            # print(self.query_tokens[0])
            # print(self.query_tokens)
            # print(self.query_tokens[0][0])
            # print(self.query_tokens[0][1])
            return self.index.get(self.query_tokens[p][0],[])
        # 去掉外层括号
        elif self.check_parentheses(p, q):
            return self.evaluate(p + 1, q - 1)
        elif self.chek_quotation(p,q):
            #print("i am called")
            return self.phrase_search(p+1,q-1)
        else:
            op = self.find_operator(p, q)
            if op == -1:
                return []
            # files1为运算符左边得到的结果，files2为右边
            if self.query_tokens[op][1] == 'NOT':
                files1 = []
            else:
                files1 = self.evaluate(p, op - 1)
            files2 = self.evaluate(op + 1, q)
            print(self.merge(files1,files2,self.query_tokens[op][1]))
            return self.merge(files1, files2, self.query_tokens[op][1])
        #sssssss

#检查双引号里面是否有其它的符号
    def chek_expr1(self,p,q):
        count = 0
        for i in range(p,q+1):
            if self.query_tokens[i][1] in ['OR','AND','NOT','YY']:
                count = count + 1
        if count != 0:
            raise Exception
        return True
#先确定除了两端意外的token_WORD,再检查两端是不是双引号
    def chek_quotation(self,p,q):
        if self.query_tokens[p][1] == 'YY' and self.query_tokens[q][1] == 'YY':
            if self.chek_expr1(p+1,q-1):
                return True
        return False

    # 判断表达式是否为 (expr)
    # 判断表达式是否为 (expr)
    def chek_expr(self, p, q):
        count = 0
        for i in range(p, q + 1):
            if self.query_tokens[i][1] == 'LP':
                count += 1
            elif self.query_tokens[i][1] == 'RP':
                count -= 1
            # 只要最后count等于0就可以判定输入合法，但先’））‘后‘（（’这种情况最后count等于零，所以在循环过程中判定count是否小于0
            if count < 0:
                return False
            #print(self.query_tokens[i][1])
        if count != 0:
            return False
        else:
            return True

    def check_parentheses(self, p, q):
        if not self.chek_expr(p, q):
            raise Exception
        if self.query_tokens[p][1] == 'LP' and self.query_tokens[q][1] == 'RP':
            if self.chek_expr(p+1,q-1):
                return True
        return False


    # 寻找表达式的dominant的运算符（优先级最低）
    def find_operator(self, p, q):
        """
        寻找表达式的dominant的运算符（优先级最低）
        其必定在括号外面（不存在整个子表达式被括号包围，前面以已处理）
        返回dominant运算符的下标位置
        """
        max_powr = 0
        max_index = -1
        count = 0
        for i in range(p, q + 1):
            if self.query_tokens[i][1] == 'LP':
                count += 1
                continue
            if self.query_tokens[i][1] == 'RP':
                count -= 1
                continue
            if count != 0:
                continue
            now_powr = token_powr[self.query_tokens[i][1]]
            if now_powr > max_powr:
                max_powr = now_powr
                max_index = i
        return max_index

    def merge(self, files1, files2, op_type):
        """
        根据运算符对进行相应的操作
        在Python中可以通过集合的操作来实现
        但为了练习算法，请遍历files1, files2合并
        """
        result = []

        if op_type == 'AND':
            result = list(set(files1) & set(files2))
        elif op_type == "OR":
            result = list(set(files1) | set(files2))
        elif op_type == "NOT":
            result = list(set(range(0, len(self.files))) - set(files2))

        return result
#创建布尔检索类对象¶
#第一次需要调用build_index()函数创建索引，之后可直接用索引文件进行初始化
br = BoolRetrieval()
br.build_index('text')
br = BoolRetrieval('index.npz','index_double.npz','index_k.npz')
br.files
br.index

while True:
    query = input("请输入与查询（与&&，或||，非！）：")
    print(br.search(query))
    #  try:
    #      query = input("请输入与查询（与&&，或||，非！）：")
    #      print(br.search(query))
    #  except(Exception):
    #      print('请检查你的输入格式,重新输入')

