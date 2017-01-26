

from invoke import task


@task
def write_manifest():
    """Write a JSON file with a list of play slugs.
    """
    print('manifest')
