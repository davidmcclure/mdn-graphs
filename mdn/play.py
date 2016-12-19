

import numpy as np
import csv
import igraph

from collections import Counter
from sklearn.preprocessing import MinMaxScaler


class Play:

    @classmethod
    def from_tsv(cls, path):

        """
        Read a TSV file.
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

        """
        Construct the graph.
        """

        self.edges = edges

        self.graph = igraph.Graph().as_directed()

        # Build set of unique speakers.
        vertices = set()
        for c1, c2 in edges.keys():
            vertices.update([c1, c2])

        # Register vertices.
        self.graph.add_vertices(list(vertices))

        # Register edges.
        for (c1, c2), weight in edges.items():
            self.graph.add_edge(c1, c2, weight=weight)

    def plot(
        self,
        fname,
        bbox=(2000, 2000),
        margin=200,
        vertex_label_size=40,
        vertex_label_dist=1,
        vertex_size_range=(10, 100),
        vertex_label_size_range=(20, 40),
        arrow_size_range=(1, 5),
        edge_width_range=(1, 10),
        **kwargs
    ):

        """
        Render the graph.
        """

        weights = np.array(self.graph.es['weight']).reshape(-1, 1)
        degrees = np.array(self.graph.degree()).reshape(-1, 1)

        # Node size
        vertex_size_scaler = MinMaxScaler(vertex_size_range)
        vertex_sizes = vertex_size_scaler.fit_transform(degrees)

        # Node size
        vertex_label_size_scaler = MinMaxScaler(vertex_label_size_range)
        vertex_label_sizes = vertex_label_size_scaler.fit_transform(degrees)

        # Arrow size
        arrow_size_scaler = MinMaxScaler(arrow_size_range)
        arrow_sizes = arrow_size_scaler.fit_transform(weights)

        # Edge width
        edge_width_scaler = MinMaxScaler(edge_width_range)
        edge_widths = edge_width_scaler.fit_transform(weights)

        # layout = self.graph.layout_fruchterman_reingold(
            # maxiter=5000,
            # weights='weight',
            # repulserad=30,
            # **kwargs
        # )

        layout = self.graph.layout_grid()

        return igraph.plot(

            self.graph,
            fname,

            margin=margin,
            bbox=bbox,

            edge_color='#aaa',
            vertex_label_dist=vertex_label_dist,

            vertex_size=vertex_sizes,
            vertex_label_size=vertex_label_sizes,
            edge_arrow_size=arrow_sizes,
            edge_width=edge_widths,

            vertex_label=self.graph.vs['name'],
            layout=layout,

        )
