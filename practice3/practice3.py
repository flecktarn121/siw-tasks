from __future__ import division
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
            self.values = values
        else:
            self.values = string_2_bag_of_words(text)


    def __str__(self):
        return str(self.values)

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values.items())

    def intersection(self, other):
        keys_a = set(self.values.keys())
        keys_b = set(other.values.keys())

        intersection_keys = keys_a & keys_b

        new_bag = {}
        for key in intersection_keys:
            new_bag[key] = 1

        return BagOfWords(values=new_bag)        

    def union(self, other):
        new_bag = {**self.values, **other.values}

        for key in new_bag.keys():
            new_bag[key] = 0
            if key in self.values:
                new_bag[key] += self.values[key]
            if key in other.values:
                new_bag[key] += other.values[key]

        return BagOfWords(values=new_bag)

class Coefficient:

    def calculate(self, bow_1, bow_2):
        self.bow_1 = bow_1
        self.bow_2 = bow_2


class Overlap(Coefficient):

    def calculate(self, bow_1, bow_2):
        super().calculate(bow_1, bow_2)
        dividend = len(self.bow_1.intersection(self.bow_2))
        divisor = min(len(self.bow_1), len(self.bow_2))

        return dividend / divisor



class Jaccard(Coefficient):

    def calculate(self, bow_1, bow_2):
        super().calculate(bow_1, bow_2)
        dividend = len(self.bow_1.intersection(self.bow_2))
        divisor = len(self.bow_1.union(self.bow_2))

        return dividend / divisor



class Cosine(Coefficient):

    def calculate(self, bow_1, bow_2):
        super().calculate(bow_1, bow_2)
        dividend = len(self.bow_1.intersection(self.bow_2))
        divisor = len(self.bow_1) * len(self.bow_2)

        return dividend / divisor


class Dice(Coefficient):

    def calculate(self, bow_1, bow_2):
        super().calculate(bow_1, bow_2)
        dividend = len(self.bow_1.intersection(self.bow_2))
        divisor = len(self.bow_1) + len(self.bow_2)

        return 2*(dividend / divisor)

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

def find_best_text(querie, texts, coefficient):
    bag1 = BagOfWords(values = querie)
    best_result = 0
    best_text = 0
    counter = 0

    for t in texts.values():
        counter += 1
        bag2 = BagOfWords(values = t)
        result = coefficient.calculate(bag1, bag2)
        if result > best_result:
            best_result = result
            best_text = counter

    return best_text

def load_lines(filename):
    f = open(filename, "r")
    lines = {}
    for line in f.readlines():
        lines[line[5:]]=string_2_bag_of_words(line[5:])
    f.close()
    return lines

#===== Auxiliary functions for the unit tests ======
def coef_dice(bow_1, bow_2):
    return Dice().calculate(bow_1, bow_2)

def coef_jaccard(bow_1, bow_2):
    return Jaccard().calculate(bow_1, bow_2)


def coef_cosine(bow_1, bow_2):
    return Cosine().calculate(bow_1, bow_2)

def coef_overlapping(bow_1, bow_2):
    return Overlap().calculate(bow_1, bow_2)
#===================================================

def main():
    texts =load_lines("cran-1400.txt")
    queries = load_lines("cran-queries.txt")
    print("# Queries' results")
    print("\nThe following results correspond to the texts that may satisfy the queries using a certain coefficient.\n")
    for querie in queries.keys():
        print("##"+querie)
        best_text = find_best_text(queries[querie], texts, Dice())

        print("- Best text with dice coefficient: " + str(best_text))
        
        best_text = find_best_text(queries[querie], texts, Jaccard())

        print("- Best text with jaccard coefficient: " + str(best_text))

        best_text = find_best_text(queries[querie], texts, Cosine())

        print("- Best text with cosine coefficient: " + str(best_text))

        best_text = find_best_text(queries[querie], texts, Overlap())

        print("- Best text with overlap coefficient: " + str(best_text))

        print("\n")

main()
