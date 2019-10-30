#!/bin/python

from __future__ import division
import nltk
import math
import argparse
import string
from InvertedIndex import InvertedIndex
nltk.download('wordnet', quiet = True)
nltk.download('stopwords', quiet = True)
nltk.download('punkt', quiet = True)
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer


class QueryTokenizer:
    ''' Class devoted to the tokenizatio of quieries'''

    def tokenize(self, query):
        ''' Tokenizes a querie by removing non alphnumeric symbols and stopwords,
            turning it to lower case and lemmatazing it

            Args:
                querie (str): the querie to be tokenized
        '''

        # Remove punctuation symbols (or simply just consider alphanumeric ones)
        text=query.translate(str.maketrans('', '', string.punctuation))  
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

class QueryManager:
    ''' Class in charge of storing the inverted index and compar the queries against it
        to offer a ranked list of results.'''

    def __init__(self, index):
        ''' The inverted index should be provided at instantiation
            Args:
                index (InvertedIndex): the inverted index of the collection'''
        self.index = index
        self.tokenizer = QueryTokenizer()

    def process_query(self, query):
        ''' Given a certain query, it will process it to give a list of ordered results
            
            Args:
                query (str): the query that needs to be solved

            Returns:
                (list of str): the ids of the documents that are thought to satisfy the querie.
                                Ordered by importance.
        '''
        terms = self.tokenizer.tokenize(query)
        documents = self.retrieve_documents(terms.keys())
        results = self.calculate_similarity(terms, documents)
        return results

    def retrieve_documents(self, terms):
        # Returns a set with the ids of the docuemnts which contains the terms
        documents = set()
        for term in terms:
            try:
                x = list(self.index.get_post_list(term).keys())
                for document in x:
                    documents.add(document)
            except ValueError:
                continue 
        return documents

    def  calculate_similarity(self, query, documents):
        # Return a list of document's ids, ordered by punctuation
        punctuations = {}
        for document in documents:
            punctuations[document] = self.cosine_similarity(query, document)
        return sorted(punctuations, key=punctuations.get)

    def cosine_similarity(self, query, document):
        similarity = 0
        dot_product = 0
        module_query = 0
        module_document = 0
        for term in query.keys():
            tf_document = self.get_tf(term, document) 
            idf = self.index.get_entry(term).get_idf #TODO: Update the index if the term is not present
            tf_query = query[term] / sum(query.values())
            dot_product +=  (idf * tf_document) * (idf * tf_query)
            module_query += math.pow((idf*tf_query), 2)
            module_document += math.pow((tf_document * idf), 2)
        module_query = math.sqrt(module_query)
        module_document = math.sqrt(module_document)
        similarity = dot_product / (module_document * module_query)
            
        return similarity

    def get_tf(self, term, document):
        try:
            return self.index.get_post_list(term)[document]
        except ValueError:
            return 0
        except KeyError:
            return 0

class DocumentIndex:
    ''' Class to store the contents of the documents of the collection'''

    def __init__(self, filename):
        ''' The name of the file containing the doucments should be provided
            
            Args:
                filename (str): name of the file containing the documents'''
        self.index = {}
        self.read_file(filename)

    def get_document(self, document_id):
        ''' Access the document for th given id

            Args:
                document_id (str): the id of the document

            Returns:
                (str): the content of the document

            Raises:
                ValueError: if the provided id do not match any entry
        '''
        if document_id not in self.index.keys():
            raise ValueError("No document with id" + document_id)
        else:
            return self.index[document_id]

    def read_file(self, filename):
        f = open(filename, "r")
        for line in f.readlines():
            elements = line.split("\t")
            self.index[elements[0].strip()] = elements[1]
        f.close()

class CLI:
    ''' Class in charge of giving a command line interface to interact with the user'''

    def __init__(self, documents, query_manager):
        self.documents = documents
        self.query_manager = query_manager
        self.options = {
                "h": lambda: self.print_options(),
                "q": lambda: self.process_query(),
                "e": lambda: exit(0),
                "c": lambda: self.display_content()
                }

    def initialize(self):
        while True:
            option = input("Enter option (press h for help):\n> ")
            self.process_option(option)

    def process_option(self, option):
        if option not in self.options.keys():
            print("\tInvalid option: " + option)
        else:
            self.options[option]()

    def print_options(self):
        print("Avaliable options:\n")
        print("\th : show help\n")
        print("\tq : write a query and show the results\n")
        print("\te : exit the program\n")
        print("\tc : display the content of a document")

    def process_query(self):
        query = input("Enter the query: ")
        results = self.query_manager.process_query(query)
        self.display_results(results)

    def display_results(self, results):
        if len(results) == 0:
            print("\tNo results found.")
            return

        print("Numer of results: " + str(len(results)))
        for doc_id in results:
            print("\t" + str(doc_id))

    def display_content(self):
        doc_id = input("Enter the document id: ")
        try:
            content = self.documents.get_document(doc_id)
            print("Content for document " + doc_id + ": \n")
            print(content)
        except ValueError:
            print("Invalid document id: " + doc_id)


def parse_args():
    parser = argparse.ArgumentParser(description="Search utility")
    parser.add_argument("file", help="Collection file, on wich each line represents a document, with the id and the document separated by a tab")
    args = parser.parse_args()
    return args

def main(args):
    print("Initializing...")
    documents = DocumentIndex(args.file)
    index = InvertedIndex()
    index.initialize(documents.index)
    query_manager = QueryManager(index)
    cli = CLI(documents, query_manager)
    print("Done")
    cli.initialize()

if __name__=="__main__":
    exit(main(parse_args()))
