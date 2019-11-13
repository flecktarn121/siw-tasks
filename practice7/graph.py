#!/bin/python

import numpy as np
import argparse
import io

class Graph:
    ''' Class representing the graph to which tha page rank will be applied'''

    def __init__(self, edges):
        self.adjacency_matrix = self._generate_adjacency_matrix(edges)
        self.dumping_factor = 0

    def _generate_adjacency_matrix(self, edges):
        # 1. Get the unique elements of the tupples
        # 2. Then, convert them to a set
        # 3. Finally to a list
        # 4. Order the list
        # 5. Iterate te list to generate a dict node -> position
        node_set = {edge[1] for edge in edges}
        nodes = {}
        counter = 0
        for node in sorted(list(node_set)):
            nodes[node] = counter
            counter += 1

        # Numpy array of zeros
        self.number_of_nodes = len(nodes)
        adjacency_matrix = np.zeros((self.number_of_nodes, self.number_of_nodes))
        for edge in edges:
            row = nodes[edge[0]]
            column = nodes[edge[1]]
            adjacency_matrix[row][column] = 1
        return adjacency_matrix

    def page_rank(self):
        ''' Calculates the page-rank for the given graph

            '''
        S = self._get_s()
        G = self._get_google_matrix(S)

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
        row_sums = matrix.sum(axis=1)
        new_matrix = matrix / row_sums[:, np.newaxis]
        return new_matrix

    def _get_google_matrix(self, S):
        aux = np.full((self.number_of_nodes, self.number_of_nodes), (1 / self.number_of_nodes))
        G = np.multiply(self.dumping_factor, S)
        G += np.multiply((1 - self.dumping_factor), aux)
        return G

def main(args):
    with io.open(args.file) as f:
        edges = list(parse_graph(f))
    graph = Graph(edges)
    print(graph.adjacency_matrix)

def parse_graph(f):
    for line in f:
        line = line.strip()
        if not line:
            continue
        src, dst = line.split(",")
        src = src.strip()
        dst = dst.strip()
        yield src, dst


def parse_args():
    parser = argparse.ArgumentParser(description='Search engine')
    parser.add_argument("file", help="Graph file")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    exit(main(parse_args()))
