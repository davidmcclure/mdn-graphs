

import re
import scandir
import os


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
