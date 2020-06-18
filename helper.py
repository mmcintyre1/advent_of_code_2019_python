from itertools import islice


def chunk(it, size):
    """Creates an iterator from a passed in iterable and builds n-sized tuples as a return."""
    it = iter(it)
    return iter(lambda: list(islice(it, size)), [])