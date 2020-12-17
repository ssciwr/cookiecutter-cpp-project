import os
from contextlib import contextmanager


@contextmanager
def inside_bake(bake):
    """
    Execute code from inside the baked cookiecutter
    """
    old_path = os.getcwd()
    try:
        os.chdir(os.path.join(bake.project.dirpath(), bake.project.basename))
        yield
    finally:
        os.chdir(old_path)
