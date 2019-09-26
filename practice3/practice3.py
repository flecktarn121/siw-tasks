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

    def __iter__(sefl):
        return iter(self.bag)





def string_2_bag_of_words(text):
    text=text.translate(str.maketrans('', '', string.punctuation))  
    # Remove punctuation symbols (or simply just consider alphanumeric ones)
    tokenizer = RegexpTokenizer(r'\w')
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
