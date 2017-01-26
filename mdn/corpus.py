

from mdn.utils import scan_paths


class Corpus:

    def __init__(self, path):
        self.path = path

    def paths(self):
        """Generate a list of TSV paths.
        """
        return scan_paths(self.path, '\.tsv')

    def rel_paths(self):
        for path in self.paths():
            yield '/'.join(path.split('/')[-2:])
