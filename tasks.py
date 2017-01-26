

import json

from invoke import task

from mdn.utils import open_makedirs
from mdn.corpus import Corpus


@task
def write_paths(ctx):
    """Write a JSON file with a list of play slugs.
    """
    c = Corpus('corpus')

    paths = list(c.rel_paths())

    with open_makedirs('site/data/paths.json', 'w') as fh:
        json.dump(paths, fh)
