from __future__ import division
import math
import string
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer


class InvertedIndex:
    ''' Class representing an inverted index, on which terms are accessed.'''

    def __init__(self):
        ''' No arguments are required for its creation. '''
        self.terms = {}
        self.number_of_documents = 0

    def put(self, term, entry):
        ''' Inserts an index entry according to the given term
            
            Args:
                term (str): the term to be inserted.
                entry (IndexEntry): the content of the entry itself.
        '''

        self.terms[term] = entry 

    def get_entry(self, term):
        '''Given a term, returns the index entry correspoding to it.
            
            Args:
                term (str): the term for which the entry is desired.

            Returns:
                entry (IndexEntry): the entry corresponding to the term.

            Raises:
                EntryError: if the trm is not contained in the index
        '''
        term_in_index(term)
        return self.terms[term]

    def update(self, term, document_id, tf):
        '''Updates the post-list for the entry of a term
            
            Args:
                term (str): '''
        self.terms[term].update_post_list(document_id, tf)

    def get_idf(self, term):
        ''' Returns the Inverse Document Frequency for a term
            
            Args:
                term (str): the term for which the IDF is wanted.

            Returns:
                float: the Inverse Document Frequency of the term.

            Raises:
                EntryError: if the term is not in the index
        '''
        self.term_in_index(term)
        return self.terms[term].get_idf()

    def get_post_list(self, term):
        ''' Returns the post_list conrresponding to the term given as an argument.
            
            Args:
                term (str): the term for which the post-list is desired.

            Returns:
                dict: a python dictionary with the ids of the documents that contains the term
                    and the corresponding Term Frequency

            Raises:
                EntryError: if th term is not in the index
        '''
        self.term_in_index(term)
        return self.terms[term].post_list
        

    def term_in_index(self, term):
        # Internal method: if the term is not in the index, raise an EntryError.
        if term not in self.terms.keys():
            raise Exception("No entry for term " + term)

    def initialize(self, documents):
        '''
        This method feeds the index with the documents corresponding to the collection.

        Args:
        documents (dict): a python dictionary on which the keys are the document's identifier, 
            and the value he string with the document's contents
        '''
        self.number_of_documents = len(documents)
        for doc_id in documents.keys():
            words = self.string_2_bag_of_words(documents[doc_id])
            for word in words.keys():
                if word not in self.terms.keys():
                    post_list = {}
                    post_list[doc_id] = words[word]
                    entry = IndexEntry(word, post_list, self.number_of_documents)
                    self.put(word, entry)
                else:
                    self.update(word, doc_id, words[word])

            
    def string_2_bag_of_words(self, text):
        #Internal method. Converts a given string to a bag of words
        # Remove punctuation symbols (or simply just consider alphanumeric ones)
        text=text.translate(str.maketrans('', '', string.punctuation))  
        tokens = nltk.word_tokenize(text)
        # get rid of stop words
        words = {}
        lemmatizer = WordNetLemmatizer()
        for token in tokens:
            token = lemmatizer.lemmatize(token.lower())
            if token not in stopwords.words('english'):
                if token not in words:
                    words[token] = 1
                else:
                    words[token] += 1

        return words

class IndexEntry:
    ''' Class representing one entry of the Inverted Index.'''

    def __init__(self, term, post_list, number_of_documents, idf = 0):
        ''' The entry should contain the term itself, plus the post_list and the idf.
            
            Args:
                term (str): the term the entry is associated with.
                post_list (dict): a python dictionary with the ids of the documents
                    which contain the term, and the corresponding TF.
                idf (float): the idf for the term, 0 by default.
        '''
        self.term = term
        self.idf = idf
        self.post_list = post_list
        self.number_of_documents = number_of_documents

    @property
    def get_idf(self):
        '''float: the current idf for a document.'''
        if self.idf == 0:
            self.update_idf()
        else:
            return self.idf

    @property
    def get_post_list(self):
        '''dict: a python dictionary with the id of the documents
               on which the term is present, and the corresponding
               Term Frequency.'''
                    
        return self.post_list

    def update_post_list(self, document_id, tf):
        # Internal method: add new documents for the entry term
        self.post_list[document_id] = tf

    def update_idf(self):
        # Internal method: update the idf for th entry term
        documents_with_term = len(self.post_list) + 1
        print(self.number_of_documents / documents_with_term)
        self.idf = math.log10(self.number_of_documents / documents_with_term) 

def read_file(filename):
    f = open(filename, "r")
    documents = {}
    for line in f.readlines():
        documents[line[:3]] = line[2:]
    f.close()
    return documents
        
def main():
    index = InvertedIndex()
    documents = read_file("documents.txt")
    index.initialize(documents)
    print(index.terms["chine"].post_list)
    print(index.terms["chine"].get_idf())

if __name__ == "__main__":
    main()
