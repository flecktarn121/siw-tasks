from __future__ import division
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

class QueryTokenizer:

    def tokenize(self, querie):
        # Remove punctuation symbols (or simply just consider alphanumeric ones)
        text=text.translate(str.maketrans('', '', string.punctuation))  
        tokens = nltk.word_tokenize(text)
        # get rid of stop words
        words = []
        lemmatizer = WordNetLemmatizer()
        for token in tokens:
            token = lemmatizer.lemmatize(token.lower())
            if token not in stopwords.words('english'):
                if token not in words:
                    words.append(token)

        return words

class QueryManager:

    def __init__(self, index):
        self.index = index
        self.tokenizer = QueryTokenizer()

    def process_query(self, query):
        terms = self.tokenizer.tokenize(query)
        entries = self.retrieve_entries(terms)
        results = self.calculate_similarity(query, entries)
        return results

    def retrieve_entries(self, terms):
        documents = []
        for term in terms:
            document = self.index.get_entry(term)
            documents.append(document)
        return documents

    def calculate_similarity(self, query, entries):
        results = []
        for term in query:
            
            
