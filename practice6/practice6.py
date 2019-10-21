
class QueryTokenizer:

    def tokenize(self, querie):
        #TODO: implement the tokenizer
        return
class QueryManager:

    def __init__(self, index):
        self.index = index
        self.tokenizer = QueryTokenizer()

    def process_query(self, query):
        terms = self.tokenizer.tokenize(query)
        documents = self.retrieve_documents(terms)
        results = self.calculate_similarity(query, documents)
        return results

    def retrieve_documents(self, terms):
        documents = []
        for term in terms:
            document = self.index.get_entry(term)
            documents.append(document)
        return documents
