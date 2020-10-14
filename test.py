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
'''
list1 = [25,1,28,5]
i = 5
if i in [5,25,,78]:
    i = i + 2
print(i)







