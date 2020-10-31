# You can add additional imports here
import sys
import pickle as pkl
import array
import os
import timeit
import contextlib


import urllib.request
import zipfile

data_url = 'http://web.stanford.edu/class/cs276/pa/pa1-data.zip'
data_dir = 'pa1-data'
urllib.request.urlretrieve(data_url, data_dir+'.zip')
zip_ref = zipfile.ZipFile(data_dir+'.zip', 'r')
zip_ref.extractall()
zip_ref.close()


try:
    os.mkdir('output_dir')
except FileExistsError:
    pass
try:
    os.mkdir('tmp')
except FileExistsError:
    pass
try:
    os.mkdir('toy_output_dir')
except FileExistsError:
    pass

sorted(os.listdir('pa1-data'))

sorted(os.listdir('pa1-data/0'))[:10]

with open('pa1-data/0/3dradiology.stanford.edu_', 'r') as f:
    print(f.read())

toy_dir = 'toy-data'


class IdMap:
    """Helper class to store a mapping from strings to ids."""

    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []

    def __len__(self):
        """Return number of terms stored in the IdMap"""
        return len(self.id_to_str)

    def _get_str(self, i):
        """Returns the string corresponding to a given id (`i`)."""
        ### Begin your code

        ### End your code

    def _get_id(self, s):
        """Returns the id corresponding to a string (`s`).
        If `s` is not in the IdMap yet, then assigns a new id and returns the new id.
        """
        ### Begin your code

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


testIdMap = IdMap()
assert testIdMap['a'] == 0, "Unable to add a new string to the IdMap"
assert testIdMap['bcd'] == 1, "Unable to add a new string to the IdMap"
assert testIdMap['a'] == 0, "Unable to retrieve the id of an existing string"
assert testIdMap[1] == 'bcd', "Unable to retrive the string corresponding to a\
                                given id"
try:
    testIdMap[2]
except IndexError as e:
    assert True, "Doesn't throw an IndexError for out of range numeric ids"
assert len(testIdMap) == 2


class UncompressedPostings:

    @staticmethod
    def encode(postings_list):
        """Encodes postings_list into a stream of bytes

        Parameters
        ----------
        postings_list: List[int]
            List of docIDs (postings)

        Returns
        -------
        bytes
            bytearray representing integers in the postings_list
        """
        return array.array('L', postings_list).tobytes()

    @staticmethod
    def decode(encoded_postings_list):
        """Decodes postings_list from a stream of bytes

        Parameters
        ----------
        encoded_postings_list: bytes
            bytearray representing encoded postings list as output by encode
            function

        Returns
        -------
        List[int]
            Decoded list of docIDs from encoded_postings_list
        """

        decoded_postings_list = array.array('L')
        decoded_postings_list.frombytes(encoded_postings_list)
        return decoded_postings_list.tolist()





x = UncompressedPostings.encode([1,2,3])
print(x)
print(UncompressedPostings.decode(x))


class InvertedIndex:
    """A class that implements efficient reads and writes of an inverted index
    to disk

    Attributes
    ----------
    postings_dict: Dictionary mapping: termID->(start_position_in_index_file,
                                                number_of_postings_in_list,
                                               length_in_bytes_of_postings_list)
        This is a dictionary that maps from termIDs to a 3-tuple of metadata
        that is helpful in reading and writing the postings in the index file
        to/from disk. This mapping is supposed to be kept in memory.
        start_position_in_index_file is the position (in bytes) of the postings
        list in the index file
        number_of_postings_in_list is the number of postings (docIDs) in the
        postings list
        length_in_bytes_of_postings_list is the length of the byte
        encoding of the postings list

    terms: List[int]
        A list of termIDs to remember the order in which terms and their
        postings lists were added to index.

        After Python 3.7 we technically no longer need it because a Python dict
        is an OrderedDict, but since it is a relatively new feature, we still
        maintain backward compatibility with a list to keep track of order of
        insertion.
    """

    def __init__(self, index_name, postings_encoding=None, directory=''):
        """
        Parameters
        ----------
        index_name (str): Name used to store files related to the index
        postings_encoding: A class implementing static methods for encoding and
            decoding lists of integers. Default is None, which gets replaced
            with UncompressedPostings
        directory (str): Directory where the index files will be stored
        """

        self.index_file_path = os.path.join(directory, index_name + '.index')
        self.metadata_file_path = os.path.join(directory, index_name + '.dict')

        if postings_encoding is None:
            self.postings_encoding = UncompressedPostings
        else:
            self.postings_encoding = postings_encoding
        self.directory = directory

        self.postings_dict = {}
        self.terms = []  # Need to keep track of the order in which the
        # terms were inserted. Would be unnecessary
        # from Python 3.7 onwards

    def __enter__(self):
        """Opens the index_file and loads metadata upon entering the context"""
        # Open the index file
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
    """
    Attributes
    ----------
    term_id_map(IdMap): For mapping terms to termIDs
    doc_id_map(IdMap): For mapping relative paths of documents (eg
        0/3dradiology.stanford.edu_) to docIDs
    data_dir(str): Path to data
    output_dir(str): Path to output index files
    index_name(str): Name assigned to index
    postings_encoding: Encoding used for storing the postings.
        The default (None) implies UncompressedPostings
    """

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
        """Base indexing code

        This function loops through the data directories,
        calls parse_block to parse the documents
        calls invert_write, which inverts each block and writes to a new index
        then saves the id maps and calls merge on the intermediate indices
        """
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
        """Parses a tokenized text file into termID-docID pairs

        Parameters
        ----------
        block_dir_relative : str
            Relative Path to the directory that contains the files for the block

        Returns
        -------
        List[Tuple[Int, Int]]
            Returns all the td_pairs extracted from the block

        Should use self.term_id_map and self.doc_id_map to get termIDs and docIDs.
        These persist across calls to parse_block
        """
        ### Begin your code

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
        """Appends the term and postings_list to end of the index file.

        This function does three things,
        1. Encodes the postings_list using self.postings_encoding
        2. Stores metadata in the form of self.terms and self.postings_dict
           Note that self.postings_dict maps termID to a 3 tuple of
           (start_position_in_index_file,
           number_of_postings_in_list,
           length_in_bytes_of_postings_list)
        3. Appends the bytestream to the index file on disk

        Hint: You might find it helpful to read the Python I/O docs
        (https://docs.python.org/3/tutorial/inputoutput.html) for
        information about appending to the end of a file.

        Parameters
        ----------
        term:
            term or termID is the unique identifier for the term
        postings_list: List[Int]
            List of docIDs where the term appears
        """
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
        """Inverts td_pairs into postings_lists and writes them to the given index

        Parameters
        ----------
        td_pairs: List[Tuple[Int, Int]]
            List of termID-docID pairs
        index: InvertedIndexWriter
            Inverted index on disk corresponding to the block
        """
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
        """Returns the next (term, postings_list) pair in the index.

        Note: This function should only read a small amount of data from the
        index file. In particular, you should not try to maintain the full
        index file in memory.
        """
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
        """Merges multiple inverted indices into a single index

        Parameters
        ----------
        indices: List[InvertedIndexIterator]
            A list of InvertedIndexIterator objects, each representing an
            iterable inverted index for a block
        merged_index: InvertedIndexWriter
            An instance of InvertedIndexWriter object into which each merged
            postings list is written out one at a time
        """
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
        """Gets a postings list (of docIds) for `term`.

        This function should not iterate through the index file.
        I.e., it should only have to read the bytes from the index file
        corresponding to the postings list for the requested term.
        """
        ### Begin your code

        ### End your code


def sorted_intersect(list1, list2):
    """Intersects two (ascending) sorted lists and returns the sorted result

    Parameters
    ----------
    list1: List[Comparable]
    list2: List[Comparable]
        Sorted lists to be intersected

    Returns
    -------
    List[Comparable]
        Sorted intersection
    """
    ### Begin your code

    ### End your code

% % tee
submission / retrieve.py


class BSBIIndex(BSBIIndex):
    def retrieve(self, query):
        """Retrieves the documents corresponding to the conjunctive query

        Parameters
        ----------
        query: str
            Space separated list of query tokens

        Result
        ------
        List[str]
            Sorted list of documents which contains each of the query tokens.
            Should be empty if no documents are found.

        Should NOT throw errors for terms not in corpus
        """
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

