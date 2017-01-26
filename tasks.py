

import json

from invoke import task

from mdn.corpus import Corpus


@task
def write_paths(ctx):
    """Write a JSON file with a list of play slugs.
    """
    c = Corpus('corpus')

    paths = list(c.rel_paths())

    with open('site/src/js/paths.json', 'w') as fh:
        json.dump(paths, fh)
