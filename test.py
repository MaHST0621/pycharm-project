'''
from collections import defaultdict
index = {}
index_f = [2,25,78]
index.setdefault('c',{})
index['c'].setdefault('nm',[])
index['c'].setdefault('nn',[])
index['c']['nm'].append(25)
index['c']['nm'].append(45)
index['c']['nm'].append(78)
index['c']['nn'].append(35)
index['c']['nn'].append(100)
index['c']['nn'].append(125)
index.setdefault('b',{})
index['b'].setdefault('jg',[])
index['b'].setdefault('gg',[])
index['b']['gg'].append(55)
index['b']['gg'].append(78)
index['b']['gg'].append(59)
index['b'].setdefault('nn',[])
d = index['b']['gg']
#list_1 = set(index['b'])
#list_0 = set(index['c'])
#print(list_1&list_0)
#index['c']['1'].append(index_f)
print(index['b']['gg'])
print(d)

index['b'] = dict
dic={}
dic.setdefault('c',{})['1']= list
dic.setdefault('c',{})['1']=2

print(dic)

from collections import defaultdict
list_1 = ['a','b','c','d','f','g','a','b','d']
list_3 = []
count = 0
list_2 = {{[]}}
for word in list_1:
    list_2['word']['1'].
print(list_3)

index = {}
list_1 = ['a', 'b', 'c', 'd', 'f', 'g', 'a', 'b', 'd']
list_2 = ['d','f','a','c','d']
num = 1
count = 0
for word in list_1:
    index.setdefault(word,{})
    index[word].setdefault(num,[])
    index[word][num].append(count)
    count = count +1
num = 2
count = 0
for word in list_2:
    index.setdefault(word,{})
    index[word].setdefault(num,[])
    index[word][num].append(count)
    count = count +1
print(index)

tokens = [('(','L'),('token','WORD'),('||','HO'),(')','R')]
count = 0
for i in range(0,len(tokens)):
    if tokens[i][0] == ')':
        count = count + 1
print(count)
print(tokens[3][0])


query_tokens = [('Fuck','WORD'),('You','WORD'),('Girl','WORD')]
result = []
result_0 = []
i = 0
for i in range(0,2):
    result_0.append((query_tokens[i][0], query_tokens[i + 1][0]))
print(result_0[0][1])

list_1 = ['a','b','c','d','f','g','a','b','a','d']
lins = []
dict1 = []
for num in range(0,len(list_1)-1):
    lins.append((list_1[num],list_1[num+1]))
for num in range(0,len(lins)):
    d = ' '.join(lins[num])
    dict1.append(d)
print(dict1)
print(lins)

index_k = {}
words = ['text','txt','ppt','to','ppa','pap','ppq','token','top']
result = []
for word in words:
    if len(word) >= 2:
        word = '$' + word + '$'
        for i in range(0, len(word) - 1):
            word_k = word[i:i + 2]
            result.append(word_k)
        for i in range(0, len(word) - 2):
            word_k = word[i:i + 3]
            result.append(word_k)
d = set(result)
print(index_k)
print(d)

list1 = ['$op','opt','pt$']
list2 = ['$op','sad']
temp = [c for c in list1 if c in list2]
temp_j = len(temp)/len((list1)+(list2)-(temp))
print(temp_j)

key_value = {}

# 初始化
# key_value[2] = 56
# key_value[1] = 2
# key_value[5] = 12
# key_value[4] = 24
# key_value[6] = 18
# key_value[3] = 323
key_value = {1:2,2:23,5:12,4:24,6:18,3:0}
print("按键(key)排序:")

# sorted(key_value) 返回重新排序的列表
# 字典按键排序
key_value = sorted(key_value.items(), key = lambda kc:kc[1],reverse=True)
b = []
for i in range (0,len(key_value[:3])):
    b.append(key_value[i][0])
print(key_value)
print(b)

list_1 = ['sad','asadsddd','aasddad','s','adasd','ss','s']
list_2 = []
len_k=len(list_1)
token = 'asdd'
for i in range(0,len(list_1)):
    if abs(len(token) - len(list_1[i])) <3 :
        list_2.append(list_1[i])
list_1 = list_2
print(list_1)
'''
token_k = 'haersadfman'
token_k = list(token_k)
token = []
for i in range(0,len(token_k)):
    if token_k[i] != token_k[i-1]:
        token.append(token_k[i])
for i in range (1,len(token)):
    if token[i] in ['a','e','i','o','u','h','w','y']:
        token[i] = '0'
    elif token[i] in ['b','f','p','v']:
        token[i] = '1'
    elif token[i] in ['c','g','j','k','q','s','x','z']:
        token[i] = '2'
    elif token[i] in ['d','t']:
        token[i] = '3'
    elif token[i] in ['l']:
        token[i] = '4'
    elif token[i] in ['m','n']:
        token[i] = '5'
    elif token[i] in ['r']:
        token[i] = '6'
result = []
for i in range(0,len(token)):
    if token[i] != '0':
        result.append(token[i])
while(len(result) < 4):
    result.append('0')
result = ''.join(result[:4])
ad = []
ad.append(result)
print(result)
print(ad)








