

import csv
import networkx as nx


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
