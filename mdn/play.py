

import csv
import numpy as np
import networkx as nx
import igraph

from sklearn.preprocessing import MinMaxScaler


class Play(nx.DiGraph):

    @classmethod
    def from_tsv(cls, path):
        """Read a TSV file.
        """
        graph = cls()

        with open(path) as fh:

            # Remove carriage returns, split on tab.
            rows = fh.read().replace('\r', '').split('\n')
            reader = csv.DictReader(rows, delimiter='\t')

            for row in reader:

                c1 = row['speaker']
                c2 = row['receiver']

                # Increment weight, if edge exists.
                if graph.has_edge(c1, c2):
                    graph[c1][c2]['weight'] += 1

                # Or, initialize edge.
                else:
                    graph.add_edge(c1, c2, weight=1)

        return graph

    def as_igraph(self):
        """Convert to igraph.
        """
        graph = igraph.Graph()

        graph.add_vertices(self.nodes())

        for c1, c2, d in self.edges(data=True):
            graph.add_edge(c1, c2, weight=d['weight'])

        return graph

    def render_igraph(
        self,
        bbox=(2000, 2000),
        margin=200,
        vertex_label_size=40,
        vertex_label_dist=1,
        vertex_size_range=(10, 100),
        vertex_label_size_range=(20, 40),
        arrow_size_range=(1, 5),
        edge_width_range=(1, 10),
    ):
        """Render with igraph.
        """
        graph = self.as_igraph()

        weights = np.array(graph.es['weight']).reshape(-1, 1)
        degrees = np.array(graph.degree()).reshape(-1, 1)

        # Node size
        vertex_size_scaler = MinMaxScaler(vertex_size_range)
        vertex_sizes = vertex_size_scaler.fit_transform(degrees)

        # Label size
        vertex_label_size_scaler = MinMaxScaler(vertex_label_size_range)
        vertex_label_sizes = vertex_label_size_scaler.fit_transform(degrees)

        # Arrow size
        arrow_size_scaler = MinMaxScaler(arrow_size_range)
        arrow_sizes = arrow_size_scaler.fit_transform(weights)

        # Edge width
        edge_width_scaler = MinMaxScaler(edge_width_range)
        edge_widths = edge_width_scaler.fit_transform(weights)

        layout = graph.layout_fruchterman_reingold(
            maxiter=5000,
            weights='weight',
            repulserad=30,
        )

        return igraph.plot(

            graph,

            margin=margin,
            bbox=bbox,

            edge_color='#aaa',
            vertex_label_dist=vertex_label_dist,

            vertex_size=vertex_sizes,
            vertex_label_size=vertex_label_sizes,
            edge_arrow_size=arrow_sizes,
            edge_width=edge_widths,

            vertex_label=graph.vs['name'],
            layout=layout,

        )
