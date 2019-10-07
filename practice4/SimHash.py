from heapq import heappush, heappop
import string
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer


def SimHash(document, restrictiveness):
    terms = string_2_bag_of_words(document).keys()
    heap = [] #will act as priority queue
    for term in terms:
        heappush(heap, hash(str(term)))
    simhash = 0
    for x in range(0, restrictiveness):
        simhash += heappop(heap)
    return simhash
    

def string_2_bag_of_words(text):
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

def getDocuments(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    file.close()
    return lines

documents = getDocuments("cran-1400.txt")
counter = 0
restrictiveness = 1
for document in documents:
    print("Hash for document number %d with restrictiveness %d", counter, restrictiveness)
    hash = SimHash(document, restrictiveness)
    print(str(hash))
    counter += 1
