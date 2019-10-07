import division from __future__
import string
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

class BagOfWords:

    def __init__(self, text="", values={}):
        if text == "":
            self.bag = values
        else:
            self.bag = string_2_bag_of_words(text)


    def __str__(self):
        return str(self.bag)

    def __len__(self):
        return len(self.bag)

    def __iter__(self):
        return iter(self.bag)

    def intersection(self, other):
        keys_a = set(self.bag.keys())
        keys_b = set(other.bag.keys())

        intersection_keys = keys_a & keys_b

        new_bag = {}
        for key in intersection_keys:
            new_bag[key] = 1

        return BagOfWords(new_bag)        

    def union(self, other):
        new_bag = {**self.bag, **other.bag}

        for key in new_bag.keys():
            new_bag[key] = 0
            if key in self.bag:
                new_bag[key] += self.bag[key]
            if key in other.bag:
                new_bag[key] += other.bag

        return BagOfWords(new_bag)

class Coefficient:
    def __init__(self, bow_1, bow_2):
        self.bow_1 = bow_1
        self.bow_2 = bow_2

    def calculate():
        return

class Overlap(Coefficient):
    def __init__(self, bow_1, bow_2):
        super().__init__(bow_1, bow_2)

    def calculate():
        dividend = len(self.bow_1.intersection(self.bow_2))
        divisor = min(len(self.bow_1), len(self.bow_2))

        return dividend / divisor



class Jaccard(Coefficient):
    def __init__(self, bow_1, bow_2):
        super().__init__(bow_1, bow_2)

    def calculate():
        dividend = len(self.bow_1.intersection(self.bow_2))
        divisor = len(self.bow_1.union(self.bow_2))

        return dividend = divisor



class Cosine(Coefficient):
    def __init__(self, bow_1, bow_2):
        super().__init__(bow_1, bow_2)

    def calculate():
        dividend = len(self.bow_1.intersection(self.bow_2))
        divisor = len(self.bow_1) * len(self.bow_2)
        

class Dice(Coefficient):
    def __init__(self, bow_1, bow_2):
        super().__init__(bow_1, bow_2)

    def calculate():
        dividend = len(self.bow_1.union(self.bow_2))
        divisor = len(self.bow_1) + len(self.bow_2)

        return 2*(dividend / divisor)

def string_2_bag_of_words(text):
    # Remove punctuation symbols (or simply just consider alphanumeric ones)
    text=text.translate(str.maketrans('', '', string.punctuation))  
    tokens = nltk.word_tokenize(text)
    print(tokens)
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

text = "Hello mr pepito! Hello mr Joseph!"
print(string_2_bag_of_words(text))
