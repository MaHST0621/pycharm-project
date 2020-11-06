# You can add additional imports here
import sys
import sys
import pickle as pkl
import array
import os
import timeit
import contextlib
import nltk
from math import log
import heapq
import urllib.request
import zipfile

# data_url = 'http://web.stanford.edu/class/cs276/pa/pa1-data.zip'
# data_dir = 'pa1-data'
# urllib.request.urlretrieve(data_url, data_dir+'.zip')
# zip_ref = zipfile.ZipFile(data_dir+'.zip', 'r')
# zip_ref.extractall()
# zip_ref.close()


# try:
#     os.mkdir('output_dir')
# except FileExistsError:
#     pass
# try:
#     os.mkdir('tmp')
# except FileExistsError:
#     pass
# try:
#     os.mkdir('toy_output_dir')
# except FileExistsError:
#     pass
#
# sorted(os.listdir('pa1-data'))
#
# sorted(os.listdir('pa1-data/0'))[:10]
#
# with open('pa1-data/0/3dradiology.stanford.edu_', 'r') as f:
#     print(f.read())
#
# toy_dir = 'toy-data'


class IdMap:

    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []

    def __len__(self):
        return len(self.id_to_str)

    def _get_str(self, i):
        return self.id_to_str[i]

    def _get_id(self, s):

        if s not in self.str_to_id.keys():
            id_need = len(self.id_to_str)
            self.id_to_str.append(s)
            return self.str_to_id.setdefault(s, id_need)
        return self.str_to_id[s]

    def __getitem__(self, key):
        if type(key) is int:
            return self._get_str(key)
        elif type(key) is str:
            return self._get_id(key)
        else:
            raise TypeError


class UncompressedPostings:
    @staticmethod
    def encode(postings_list):

        return array.array('L', postings_list).tobytes()

    @staticmethod
    def decode(encoded_postings_list):
        decoded_postings_list = array.array('L')
        decoded_postings_list.frombytes(encoded_postings_list)
        return decoded_postings_list.tolist()


class InvertedIndex:

    def __init__(self, index_name, postings_encoding=None, directory=''):

        self.index_file_path = os.path.join(directory, index_name + '.index')
        self.metadata_file_path = os.path.join(directory, index_name + '.dict')

        if postings_encoding is None:
            self.postings_encoding = UncompressedPostings
        else:
            self.postings_encoding = postings_encoding
        self.directory = directory

        self.postings_dict = {}
        self.terms = []
    def __enter__(self):

        self.index_file = open(self.index_file_path, 'rb+')

        with open(self.metadata_file_path, 'rb') as f:
            self.postings_dict, self.terms = pkl.load(f)
            self.term_iter = self.terms.__iter__()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.index_file.close()
        with open(self.metadata_file_path, 'wb') as f:
            pkl.dump([self.postings_dict, self.terms], f)

class BSBIIndex:
    def __init__(self, data_dir, output_dir, index_name="BSBI",postings_encoding=None):
        self.term_id_map = IdMap()
        self.doc_id_map = IdMap()
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.index_name = index_name
        self.postings_encoding = postings_encoding
        self.intermediate_indices = []

    def save(self):
        with open(os.path.join(self.output_dir, 'terms.dict'), 'wb') as f:
            pkl.dump(self.term_id_map, f)
        with open(os.path.join(self.output_dir, 'docs.dict'), 'wb') as f:
            pkl.dump(self.doc_id_map, f)

    def load(self):
        with open(os.path.join(self.output_dir, 'terms.dict'), 'rb') as f:
            self.term_id_map = pkl.load(f)
        with open(os.path.join(self.output_dir, 'docs.dict'), 'rb') as f:
            self.doc_id_map = pkl.load(f)

    def index(self):
        for block_dir_relative in sorted(next(os.walk(self.data_dir))[1]):
            td_pairs = self.parse_block(block_dir_relative)
            index_id = 'index_' + block_dir_relative
            self.intermediate_indices.append(index_id)
            with InvertedIndexWriter(index_id, directory=self.output_dir,postings_encoding=self.postings_encoding) as index:
                self.invert_write(td_pairs, index)
                td_pairs = None
        self.save()
        with InvertedIndexWriter(self.index_name, directory=self.output_dir,postings_encoding=self.postings_encoding) as merged_index:
            with contextlib.ExitStack() as stack:
                indices = [stack.enter_context(InvertedIndexIterator(index_id,directory=self.output_dir,postings_encoding=self.postings_encoding))
                    for index_id in self.intermediate_indices]
                self.merge(indices, merged_index)
class BSBIIndex(BSBIIndex):
    def parse_block(self, block_dir_relative):
        word_doc = []
        doc_path = self.data_dir + '/' + block_dir_relative + '/'
        for i in os.listdir(doc_path):
            doc_id = self.doc_id_map[doc_path + i]
        f = open(doc_path + i)
        for line in f.readlines():
            for terms in line.strip().split(' '):
                print(terms, i)
                word_doc.append((self.term_id_map[terms], doc_id))
        return word_doc


class InvertedIndexWriter(InvertedIndex):
    def __enter__(self):
        self.index_file = open(self.index_file_path, 'wb+')
        return self

    def append(self, term, postings_list):
        encoded_postings_list = self.postings_encoding.encode(postings_list)
        self.terms.append(term)
        self.postings_dict[term] = (self.index_file.tell(), len(postings_list), len(encoded_postings_list))
        self.index_file.write(encoded_postings_list)
class BSBIIndex(BSBIIndex):
    def invert_write(self, td_pairs, index):
        term_id = -1
        postings_list = []
        for pair in sorted(set(td_pairs)):
            if pair[0] != term_id:
                if term_id != -1:
                    index.append(term_id, postings_list)
                term_id = pair[0]
                postings_list = []
            postings_list.append(pair[1])
        index.append(term_id, postings_list)


class InvertedIndexIterator(InvertedIndex):
    def __enter__(self):
        super().__enter__()
        self._initialization_hook()
        return self

    def _initialization_hook(self):
        self.term_idx = 0
    def __iter__(self):
        return self

    def __next__(self):
        if self.term_idx == len(self.terms):
            raise StopIteration
        term = self.terms[self.term_idx]
        self.term_idx = self.term_idx + 1
        pos, length, size = self.postings_dict[term]
        self.index_file.seek(pos)
        return (term, self.postings_encoding.decode(self.index_file.read(size)))
    def delete_from_disk(self):
        self.delete_upon_exit = True

    def __exit__(self, exception_type, exception_value, traceback):
        self.index_file.close()
        if hasattr(self, 'delete_upon_exit') and self.delete_upon_exit:
            os.remove(self.index_file_path)
            os.remove(self.metadata_file_path)
        else:
            with open(self.metadata_file_path, 'wb') as f:
                pkl.dump([self.postings_dict, self.terms], f)

class BSBIIndex(BSBIIndex):
    def merge(self, indices, merged_index):
        term_id = -1
        postings_list = []
        for pair in heapq.merge(*indices, key=lambda x: x[0]):
            if pair[0] != term_id:
                if term_id != -1:
                    merged_index.append(term_id, sorted(set(postings_list)))
                term_id = pair[0]
                postings_list = []
            postings_list += pair[1]
        merged_index.append(term_id, sorted(set(postings_list)))


class InvertedIndexMapper(InvertedIndex):
    def __getitem__(self, key):
        return self._get_postings_list(key)

    def _get_postings_list(self, term):
        pos, length, size = self.postings_dict[term]
        self.index_file.seek(pos)
        return self.postings_encoding.decode(self.index_file.read(size))

def sorted_intersect(list1, list2):

    ret = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            i += 1
        elif list2[j] < list1[i]:
            j += 1
        else:
            ret.append(list1[i])
            i += 1
            j += 1
    return ret


class BSBIIndex(BSBIIndex):
    def retrieve(self, query):
        if len(self.term_id_map) == 0 or len(self.doc_id_map) == 0:
            self.load()
        intersected = False
        intersected_postings = []
        with InvertedIndexMapper('BSBI', directory=self.output_dir) as index_mapper:
            for token in query.split(' '):
                if intersected:
                    intersected_postings = sorted_intersect(index_mapper[self.term_id_map[token]], intersected_postings)
                else:
                    intersected_postings = index_mapper[self.term_id_map[token]]
                    intersected = True


class CompressedPostings:
    def encode_int(gap):
        ret = [(gap & 0x7f) | 0x80]
        gap >>= 7
        while gap != 0:
            ret.insert(0, gap & 0x7f)
            gap >>= 7
        return ret

    @staticmethod
    def encode(postings_list):
        encoded_postings_list = []
        encoded_postings_list += CompressedPostings.encode_int(postings_list[0])
        for i in range(1, len(postings_list)):
            encoded_postings_list += CompressedPostings.encode_int(postings_list[i] - postings_list[i - 1])
        return array.array('B', encoded_postings_list).tobytes()

    @staticmethod
    def decode(encoded_postings_list):
        decoded_postings_list = array.array('B')
        decoded_postings_list.frombytes(encoded_postings_list)

        postings_list = []
        base, n = 0, len(decoded_postings_list)
        idx = 0
        while idx < n:
            gap = 0
            while idx < n and (decoded_postings_list[idx] & 0x80) == 0:
                gap = (gap << 7) | (decoded_postings_list[idx] & 0x7f)
                idx += 1
            gap = (gap << 7) | (decoded_postings_list[idx] & 0x7f)
            idx += 1

            posting = base + gap
            postings_list.append(posting)
            base = posting
        return postings_list


class ECCompressedPostings:
    def encode_int(gap):
        if gap == 0 or gap == 1:
            return '0'
        ret = '1' * int(log(gap, 2)) + '0' + bin(gap)[3:]
        print(ret)
        return ret

    @staticmethod
    def encode(postings_list):
        encoded_postings_list = ''
        encoded_postings_list += ECCompressedPostings.encode_int(postings_list[0] - (-1))
        for i in range(1, len(postings_list)):
            encoded_postings_list += ECCompressedPostings.encode_int(postings_list[i] - postings_list[i - 1])
        print(encoded_postings_list)
        return array.array('B', [int(encoded_postings_list[x:x + 8], 2) for x in
                                 range(0, len(encoded_postings_list), 8)]).tobytes()

    @staticmethod
    def decode(encoded_postings_list):
        decoded_bytes_list = array.array('B')
        decoded_bytes_list.frombytes(encoded_postings_list)

        decoded_postings_list = ''.join([bin(x)[2:].zfill(8) for x in decoded_bytes_list])
        decoded_postings_list = decoded_postings_list[:-7] + bin(decoded_bytes_list[-1])[2:]
        print(decoded_postings_list)

        postings_list = []
        base, idx, n = -1, 0, len(decoded_postings_list)
        while idx < n:
            length = 0
            while idx < n and decoded_postings_list[idx] == '1':
                length += 1
                idx += 1
            if idx < n:
                # '111...1(length)0xxx...x(length)', length maybe 0
                idx = idx + 1 + length
                gap = int('1' + decoded_postings_list[idx - length: idx], 2)
                posting = base + gap
                postings_list.append(posting)
                base = posting
        return postings_list
try:
    os.mkdir('output_dir_ECCcompressed')
except FileExistsError:
    pass

BSBI_instance_compressed = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir_ECCcompressed', postings_encoding=ECCompressedPostings)
BSBI_instance_compressed.index()
