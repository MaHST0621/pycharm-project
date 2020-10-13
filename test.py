'''
from collections import defaultdict
index = {}
index_f = [2,25,78]
index.update({'c':{}})
index['c']['2'] = []
index['c']['2'].append(25)
index['c']['2'].append(35)
#index['c']['1'].append(index_f)
print(index)

index['b'] = dict
dic={}
dic.setdefault('b',{})['1']= list
dic.setdefault('b',{})['c']=2

print(dic)

from collections import defaultdict
list_1 = ['a','b','c','d','f','g','a','b','d']
list_3 = []
count = 0
list_2 = {{[]}}
for word in list_1:
    list_2['word']['1'].
print(list_3)
'''
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



