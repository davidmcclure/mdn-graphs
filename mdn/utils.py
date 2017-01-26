

import re
import scandir
import os
import attr

from contextlib import contextmanager


def scan_paths(root_dir, pattern):

    """
    Walk a directory and yield file paths that match a pattern.
    """

    root_dir = os.path.abspath(root_dir)

    pattern = re.compile(pattern)

    for root, dirs, files in scandir.walk(root_dir, followlinks=True):
        for name in files:

            # Match the extension.
            if pattern.search(name):
                yield os.path.join(root, name)


@attr.s
class LinearScale(object):

    d1 = attr.ib()
    d2 = attr.ib()
    r1 = attr.ib()
    r2 = attr.ib()

    def __call__(self, val):
        """Map a value from domain interval onto the range.

        Args:
            val (int)
        """
        ratio = float(val-self.d1) / (self.d2-self.d1)
        return self.r1 + ratio*(self.r2-self.r1)


@contextmanager
def open_makedirs(fpath, *args, **kwargs):

    """
    Create the directory for a file, open it.
    """

    path = os.path.dirname(fpath)

    if not os.path.exists(path):
        os.makedirs(path)

    with open(fpath, *args, **kwargs) as fh:
        yield fh
