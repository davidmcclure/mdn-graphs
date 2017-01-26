

import json

from invoke import task

from mdn.utils import open_makedirs
from mdn.play import Play
from mdn.corpus import Corpus


corpus = Corpus('corpus')


@task
def write_paths(ctx):
    """Write a JSON file with a list of play slugs.
    """
    paths = list(corpus.rel_paths())

    with open_makedirs('site/data/paths.json', 'w') as fh:
        json.dump(paths, fh)
