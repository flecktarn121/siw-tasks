import numpy as np

class Graph:
    ''' Class representing the graph to which tha page rank will be applied'''

    def __init__(self, edges):
        self.adjacency_matrix = self.generate_adjacency_matrix(edges)

    def generate_adjacency_matrix(self, edges):
        # 1. Generate tupples for the list of edges.
        # 2. Then, convert them to a set
        # 3. Finally to a list
        # 4. Order the list
        # 5. Iterate te list to generate a dict node -> position
        node_tuples = [tuple(node) for node in edges]
        nodes = {}
        counter = 0
        for node in sort(list(set(node_tuples))):
            nodes[node] = counter
            counter += 1

        adjacency_matrix = np.zeros(len(nodes), len(nodes))
        for edge in edges:
            row = nodes[edge[0]]
            column = nodes[edge[1]]
            adjacency_matrix[row][column] = 1
