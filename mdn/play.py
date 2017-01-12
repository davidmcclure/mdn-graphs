

import numpy as np
import csv
import igraph

from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from graphviz import Digraph


class LinearScale:

    def __init__(self, domain, range_):
        self.domain = domain
        self.range = range_

    def __call__(self, val):
        ratio = float(val - self.domain[0]) / (self.domain[1] - self.domain[0])
        return self.range[0] + ratio*(self.range[1]-self.range[0])


class Play:

    @classmethod
    def from_tsv(cls, path):
        """Read a TSV file.
        """
        with open(path) as fh:

            # Remove carriage returns from speeches.
            rows = fh.read().replace('\r', '').split('\n')

            reader = csv.DictReader(rows, delimiter='\t')

            edges = Counter()

            for row in reader:
                edges[row['speaker'], row['receiver']] += 1

        return cls(edges)

    def __init__(self, edges):
        """Construct the graph.
        """
        self.graph = Digraph(
            engine='neato',
            graph_attr=dict(
                splines='true',
                concentrate='true',
                overlap='false',
                dir='both',
            )
        )

        weights = list(edges.values())

        edge_scale = LinearScale(
            (min(weights), max(weights)),
            (1, 5),
        )

        for (c1, c2), count in edges.items():
            self.graph.edge(c1, c2, arrowsize=str(edge_scale(count)))
