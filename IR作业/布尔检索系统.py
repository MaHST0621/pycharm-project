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
lexer = re.compile('|'.join([token_or, token_not, token_word,
                            token_and, token_lp, token_rp]))  # 编译正则表达式
# 用编译好的正则表达式进行词法分析
def get_tokens(query):
    tokens = []  # tokens中的元素类型为(token, token类型)
    for token in re.finditer(lexer, query):
        tokens.append((token.group(), token.lastgroup))
    print(tokens)
    return tokens
#创建一个字典类型记录符号权重
token_powr = {'WORD':0,'NOT':3,'AND':2,'OR':1}


class BoolRetrieval:
    """
    布尔检索类
    index为字典类型，其键为单词，值为文件ID列表，如{"word": [1, 2, 9], ...}
    """
#sssssssss
    def __init__(self, index_path=''):
        if index_path == '':
            self.index = defaultdict(list)
            self.f_index = defaultdict(list)
        # 已有构建好的索引文件
        else:
            data = np.load(index_path, allow_pickle=True)
            self.files = data['files'][()]
            self.index = data['index'][()]
        self.query_tokens = []
        print(self.query_tokens)

    def build_index(self, text_dir):
        self.files = get_files(text_dir)  # 获取所有文件名
        for num in range(0, len(self.files)):
            f = open(self.files[num])
            text = f.read()
            words = get_words(text)  # 分词
            # 构建倒排索引
            for word in words:
                count = 0
                count =count +1
                self.f_index[word].append(count)
                self.index[word].append(num)

        print(self.files, self.index)
        print(self.index)
        np.savez('index.npz', files=self.files, index=self.index,f_index=self.f_index)

    def search(self, query):
        self.query_tokens = get_tokens(query)  # 获取查询的tokens
        print(self.query_tokens)
        result = []
        # 将查询得到的文件ID转换成文件名
        for num in self.evaluate(0, len(self.query_tokens) - 1):
            result.append(self.files[num])
        return result

    def phrase_search(self,p,q):
        print('先放着吧')

    # 递归解析布尔表达式，p、q为子表达式左右边界的下标
    def evaluate(self, p, q):
        # 解析错误
        if p > q:
            return []
        # 单个token，一定为查询词
        elif p == q:
            #print(self.query_tokens[p][0])
            #print(self.query_tokens[p][1])
            return self.index[self.query_tokens[p][0]]
        # 去掉外层括号
        elif self.check_parentheses(p, q):
            return self.evaluate(p + 1, q - 1)
        elif self.chek_quotation(p,q):
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
            #print(self.merge(files1,files2,self.query_tokens[op][1]))
            return self.merge(files1, files2, self.query_tokens[op][1])
        #sssssss

#检查双引号里面
    def chek_expr1(self,p,q):
        for i in range(p,q+1):
            if self.query_tokens[i][0] != 'WORD':
                return False
#先确定除了两端意外的token_WORD,再检查两端是不是双引号
    def chek_quotation(self,p,q):
        if self.chek_expr1(p+1,q-1):
            if self.query_tokens[p][0] == '"' and self.query_tokens[q+1][0] == '"':
                return True
            else:
                return False

    # 判断表达式是否为 (expr)
    # 判断表达式是否为 (expr)
    def chek_expr(self, p, q):
        count = 0
        for i in range(p, q + 1):
            if self.query_tokens[i][0] == '(':
                count += 1
            elif self.query_tokens[i][0] == ')':
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
        if self.chek_expr(p, q):
            if self.query_tokens[p][0] == '(' and self.query_tokens[q][0] == ')':
                return True
            else:
                return False
        else:
            raise Exception

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
            if self.query_tokens[i][1] == '(':
                count += 1
                continue
            if self.query_tokens[i][1] == ')':
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
#br = BoolRetrieval()
#br.build_index('text')
br = BoolRetrieval('index.npz')
br.files
br.index
while True:
    try:
        query = input("请输入与查询（与&&，或||，非！）：")
        print(br.search(query))
    except:
        print('请检查你的输入格式,重新输入')
