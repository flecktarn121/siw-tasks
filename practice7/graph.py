#!/bin/python

import numpy as np

class Graph:
    ''' Class representing the graph to which tha page rank will be applied'''

    def __init__(self, edges):
        self.rank = {}
        self.adjacency_matrix = self._generate_adjacency_matrix(edges)

    def _generate_adjacency_matrix(self, edges):
        # 1. Get the unique elements of the tupples
        # 2. Then, convert them to a set
        # 3. Finally to a list
        # 4. Order the list
        # 5. Iterate te list to generate a dict node -> position
        node_set = {edge[1] for edge in edges}
        node_set = node_set.union({edge[0] for edge in edges})
        nodes = {}
        counter = 0
        for node in sorted(list(node_set)):
            nodes[node] = counter
            self.rank[node] = 0
            counter += 1

        # Numpy array of zeros
        self.number_of_nodes = len(nodes)
        adjacency_matrix = np.zeros((self.number_of_nodes, self.number_of_nodes))
        for edge in edges:
            row = nodes[edge[0]]
            column = nodes[edge[1]]
            adjacency_matrix[row][column] = 1
        return adjacency_matrix

    def page_rank(self, damping=0.75, limit=1.0e-8):
        ''' Calculates the page-rank for the given graph

                Args:
                    damping (real): the damping factor for the algorithm
                    limit (real): the acceptable error for each iteration

                Returns:
                    (dict): a dictionary on which the key is the node, and the value its pagerank
        '''
        S = self._get_s()
        G = self._get_google_matrix(S, damping)

        # First iteration done manually
        x0 = np.full((1, self.number_of_nodes), (1 / self.number_of_nodes))
        x = np.dot(x0, G)

        # The quadratic error corresponds to norm 2
        while np.linalg.norm(x - x0, 2) > limit:
            x0 = x
            x = np.dot(x0, G)
        counter = 0
        for node in self.rank.keys():
            self.rank[node] = x[0, counter]
            counter += 1
        return self.rank

    def _get_s(self):
        # Returns the stochastic matrix of the adjacency matrix,
        # that is, all-zero rows are subsituted by 1/n*nodes

        h = self._normalize(self.adjacency_matrix)
        zeroes = np.where(~h.any(axis=1))[0]
        for row in zeroes:
            h[row] = (1 / self.number_of_nodes)
        return h

    def _normalize(self, matrix):
        # Normalize the given matrix

        cols = matrix.sum(axis=1)
        # If one of the rows is all 0, they will result in nan
        new_matrix = matrix / row_sums[:, np.newaxis]
        # Substitute nan by 0
        new_matrix[np.isnan(new_matrix)] = 0
        return new_matrix

    def _get_google_matrix(self, S, damping):
        # Return th google matrix, applying the damping factor

        aux = np.full((self.number_of_nodes, self.number_of_nodes), (1 / self.number_of_nodes))
        G = damping * S + (1 - damping) * aux
        return G
