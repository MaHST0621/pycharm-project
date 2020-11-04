# You can add additional imports here
import sys
import pickle as pkl
import array
import os
import timeit
import contextlib
i = 0

##import urllib.request
##import zipfile

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
    """Helper class to store a mapping from strings to ids."""

    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []
        global id_nedd


    def __len__(self):
        """Return number of terms stored in the IdMap"""
        return len(self.id_to_str)

    def _get_str(self, i):
        """Returns the string corresponding to a given id (`i`)."""
        ### Begin your code
        return self.id_to_str[i]
        ### End your code

    def _get_id(self, s):
        """Returns the id corresponding to a string (`s`).
        If `s` is not in the IdMap yet, then assigns a new id and returns the new id.
        """

        ### Begin your code
        if s not in self.str_to_id.keys():
            Id_need = len(self.id_to_str)
            self.id_to_str.append(s)
            return self.str_to_id.setdefault(s,Id_need)
        return self.str_to_id[s]
        ### End your code

    def __getitem__(self, key):
        """If `key` is a integer, use _get_str;
           If `key` is a string, use _get_id;"""
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

        # Load the postings dict and terms from the metadata file
        with open(self.metadata_file_path, 'rb') as f:
            self.postings_dict, self.terms = pkl.load(f)
            self.term_iter = self.terms.__iter__()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Closes the index_file and saves metadata upon exiting the context"""
        # Close the index file
        self.index_file.close()

        # Write the postings dict and terms to the metadata file
        with open(self.metadata_file_path, 'wb') as f:
            pkl.dump([self.postings_dict, self.terms], f)


# Do not make any changes here, they will be overwritten while grading
class BSBIIndex:


    def __init__(self, data_dir, output_dir, index_name="BSBI",
                 postings_encoding=None):
        self.term_id_map = IdMap()
        self.doc_id_map = IdMap()
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.index_name = index_name
        self.postings_encoding = postings_encoding

        # Stores names of intermediate indices
        self.intermediate_indices = []

    def save(self):
        """Dumps doc_id_map and term_id_map into output directory"""

        with open(os.path.join(self.output_dir, 'terms.dict'), 'wb') as f:
            pkl.dump(self.term_id_map, f)
        with open(os.path.join(self.output_dir, 'docs.dict'), 'wb') as f:
            pkl.dump(self.doc_id_map, f)

    def load(self):
        """Loads doc_id_map and term_id_map from output directory"""

        with open(os.path.join(self.output_dir, 'terms.dict'), 'rb') as f:
            self.term_id_map = pkl.load(f)
        with open(os.path.join(self.output_dir, 'docs.dict'), 'rb') as f:
            self.doc_id_map = pkl.load(f)

    def index(self):

        for block_dir_relative in sorted(next(os.walk(self.data_dir))[1]):
            td_pairs = self.parse_block(block_dir_relative)
            index_id = 'index_' + block_dir_relative
            self.intermediate_indices.append(index_id)
            with InvertedIndexWriter(index_id, directory=self.output_dir,
                                     postings_encoding=
                                     self.postings_encoding) as index:
                self.invert_write(td_pairs, index)
                td_pairs = None
        self.save()
        with InvertedIndexWriter(self.index_name, directory=self.output_dir,
                                 postings_encoding=
                                 self.postings_encoding) as merged_index:
            with contextlib.ExitStack() as stack:
                indices = [stack.enter_context(
                    InvertedIndexIterator(index_id,
                                          directory=self.output_dir,
                                          postings_encoding=
                                          self.postings_encoding))
                    for index_id in self.intermediate_indices]
                self.merge(indices, merged_index)


class BSBIIndex(BSBIIndex):
    def parse_block(self, block_dir_relative):

        ### Begin your code
        word_doc = []
        doc_path = self.data_dir + '/' + block_dir_relative + '/'
        for i in os.listdir(doc_path):
            doc_id = self.doc_id_map[doc_path + i]
            f = open(doc_path + i)
        #     words = f.read()
        #
        #     for word in words:
        #         print(word,doc_id)
        #         word_doc.append(self.term_id_map[word],doc_id)
        # return word_doc
            for line in f.readlines():
                for word in line.strip().split(' '):
                    print(word,i)
                    word_doc.append((self.term_id_map[word],doc_id))
        return word_doc
        ### End your code




with open('toy-data/0/fine.txt', 'r') as f:
    print(f.read())
with open('toy-data/0/hello.txt', 'r') as f:
    print(f.read())


BSBI_instance = BSBIIndex(data_dir=toy_dir, output_dir = 'tmp/', index_name = 'toy')
BSBI_instance.parse_block('0')


### Begin your code

### End your code


class InvertedIndexWriter(InvertedIndex):
    """"""

    def __enter__(self):
        self.index_file = open(self.index_file_path, 'wb+')
        return self

    def append(self, term, postings_list):

        ### Begin your code

        ### End your code




with InvertedIndexWriter('test', directory='tmp/') as index:
    index.append(1, [2, 3, 4])
    index.append(2, [3, 4, 5])
    index.index_file.seek(0)
    assert index.terms == [1,2], "terms sequence incorrect"
    assert index.postings_dict == {1: (0, 3, len(UncompressedPostings.encode([2,3,4]))),
                                   2: (len(UncompressedPostings.encode([2,3,4])), 3,
                                       len(UncompressedPostings.encode([3,4,5])))}, "postings_dict incorrect"
    assert UncompressedPostings.decode(index.index_file.read()) == [2, 3, 4, 3, 4, 5], "postings on disk incorrect"


class BSBIIndex(BSBIIndex):
    def invert_write(self, td_pairs, index):

        ### Begin your code

        ### End your code





### Begin your code

### End your code


class InvertedIndexIterator(InvertedIndex):
    """"""

    def __enter__(self):
        """Adds an initialization_hook to the __enter__ function of super class
        """
        super().__enter__()
        self._initialization_hook()
        return self

    def _initialization_hook(self):
        """Use this function to initialize the iterator
        """
        ### Begin your code

        ### End your code

    def __iter__(self):
        return self

    def __next__(self):

        ### Begin your code

        ### End your code

    def delete_from_disk(self):
        """Marks the index for deletion upon exit. Useful for temporary indices
        """
        self.delete_upon_exit = True

    def __exit__(self, exception_type, exception_value, traceback):
        """Delete the index file upon exiting the context along with the
        functions of the super class __exit__ function"""
        self.index_file.close()
        if hasattr(self, 'delete_upon_exit') and self.delete_upon_exit:
            os.remove(self.index_file_path)
            os.remove(self.metadata_file_path)
        else:
            with open(self.metadata_file_path, 'wb') as f:
                pkl.dump([self.postings_dict, self.terms], f)






### Begin your code

### End your code



import heapq
animal_lifespans = [('Giraffe', 28),
                   ('Rhinoceros', 40),
                   ('Indian Elephant', 70),
                   ('Golden Eagle', 80),
                   ('Box turtle', 123)]

tree_lifespans = [('Gray Birch', 50),
                  ('Black Willow', 70),
                  ('Basswood', 100),
                  ('Bald Cypress', 600)]

lifespan_lists = [animal_lifespans, tree_lifespans]

for merged_item in heapq.merge(*lifespan_lists, key=lambda x: x[1]):
    print(merged_item)

import heapq


class BSBIIndex(BSBIIndex):
    def merge(self, indices, merged_index):

        ### Begin your code

        ### End your code


BSBI_instance = BSBIIndex(data_dir=toy_dir, output_dir = 'toy_output_dir', )
BSBI_instance.index()

BSBI_instance = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir', )
BSBI_instance.index()


BSBI_instance = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir', )
BSBI_instance.intermediate_indices = ['index_'+str(i) for i in range(10)]
with InvertedIndexWriter(BSBI_instance.index_name, directory=BSBI_instance.output_dir, postings_encoding=BSBI_instance.postings_encoding) as merged_index:
    with contextlib.ExitStack() as stack:
        indices = [stack.enter_context(InvertedIndexIterator(index_id, directory=BSBI_instance.output_dir, postings_encoding=BSBI_instance.postings_encoding)) for index_id in BSBI_instance.intermediate_indices]
        BSBI_instance.merge(indices, merged_index)


class InvertedIndexMapper(InvertedIndex):
    def __getitem__(self, key):
        return self._get_postings_list(key)

    def _get_postings_list(self, term):

        ### Begin your code

        ### End your code


def sorted_intersect(list1, list2):


% % tee
submission / retrieve.py


class BSBIIndex(BSBIIndex):
    def retrieve(self, query):

        if len(self.term_id_map) == 0 or len(self.doc_id_map) == 0:
            self.load()

        ### Begin your code

        ### End your code



BSBI_instance = BSBIIndex(data_dir='pa1-data', output_dir = 'output_dir', )
BSBI_instance.retrieve('boolean retrieval')


with open("pa1-data/1/cs276.stanford.edu_", 'r') as f:
    print(f.read())


for i in range(1, 9):
    with open('dev_queries/query.' + str(i)) as q:
        query = q.read()
        my_results = [os.path.normpath(path) for path in BSBI_instance.retrieve(query)]
        with open('dev_output/' + str(i) + '.out') as o:
            reference_results = [os.path.normpath(x.strip()) for x in o.readlines()]
            assert my_results == reference_results, "Results DO NOT match for query: "+query.strip()
        print("Results match for query:", query.strip())


set(my_results) - set(reference_results)

set(reference_results) - set(my_results)

