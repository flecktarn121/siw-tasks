class InvertedIndex:
    def __init__(self):
        self.terms = {}

    def put(self, term, idf, post_list):
        values = []
        values.append(idf)
        values.append(post_list)
        self.terms[term] = values 

    def get_idf(self, term):
        self.term_in_index(term)
        return self.terms[term](0)

    def get_post_list(self, term):
        self.term_in_index(term)
        return self.terms[term](1)
        

    def term_in_index(self, term):
        if term not in self.terms.keys():
            raise Exception("No entry for term " + term)

    def initialize(self, documents):
        for document in documents:
            

