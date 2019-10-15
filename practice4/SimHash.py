import json
import gzip
from heapq import heappush, heappop
import string
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import hashlib

def sim_hash(document, restrictiveness):
    '''Returns the similarity hash of a document for a given restrictiviness level'''
    
    terms = string_2_bag_of_words(document).keys()
    heap = [] #will act as priority queue
    for term in terms:
        heappush(heap, md5_hash(str(term)))
    simhash = 0
    for x in range(0, restrictiveness):
        if len(heap) <= 0:
            break
        simhash += heappop(heap)
    return simhash

def md5_hash(text):
    '''Generates a deterministic hash with md5 algorithm'''
    return int(hashlib.md5(text.encode("utf8")).hexdigest(), 16)

def string_2_bag_of_words(text):
    '''Converts a given string into a bag of words, applying:
            -tokenization
            -elimination of stop words
            -lematization
            -conversion into lower keys
        '''
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

def get_documents(filename):
    '''Reads a text file on which each line is a document'''
    f = open(filename, "r")
    lines = []
    for line in f.readlines():
        lines.append(line[5:])
    f.close()
    return lines

def get_json(filename):
    '''Reads a compressed json file on which each line corresponds
    to a tweet.'''
    documents = []
    with gzip.GzipFile(filename, "r") as fin:
        for line in fin:
            line_str = line.decode("utf-8")
            tweet = json.loads(line_str)
            if tweet["_source"]["lang"] == "en":
                documents.append(tweet["_source"]["text"])
    return documents


def main():
    #documents = getDocuments("cran-1400.txt")
    documents = getJson("2008-Feb-02-04.json.gz")
    counter = 0
    restrictiveness = 8 
    similar_documents = {}

    for document in documents:
        text_hash = sim_hash(document, restrictiveness)
        if text_hash not in similar_documents.keys():
            similar_documents[text_hash] = []
        similar_documents[text_hash].append(document)

    print("# Results\n")
    print("The following documents have been found similar according to the _simhash_ system with restrictiveness " + str(restrictiveness) + ".\n")

    for simhash in similar_documents.keys():
        if len(similar_documents[simhash]) > 1:
            print("\n## Hash "+ str(simhash) + "\n")
            for document in similar_documents[simhash]:
                print("- " + document)

if __name__ == "__main__":
    main()
