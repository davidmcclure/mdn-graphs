

import json
import os

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


@task
def write_plays(ctx):
    """Write each play as JSON for d3.
    """
    paths = list(corpus.paths())

    rel_paths = list(corpus.rel_paths())

    for path, rel_path in zip(paths, rel_paths):

        try:
            play = Play.from_tsv(path)
        except:
            continue

        out_path = os.path.join('site/data/plays', rel_path)

        with open_makedirs(out_path, 'w') as fh:
            json.dumps(play.as_d3_data(), fh)
            print(rel_path)
