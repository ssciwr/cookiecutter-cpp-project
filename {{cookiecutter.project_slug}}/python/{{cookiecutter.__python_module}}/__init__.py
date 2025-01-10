from _{{ cookiecutter|modname }} import add_one

# Export the version given in project metadata
from importlib import metadata
__version__ = metadata.version(__package__)
del metadata


def one_plus_one():
    return add_one(1)
