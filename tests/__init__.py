import os
import time
from contextlib import contextmanager


@contextmanager
def inside_bake(bake):
    """
    Execute code from inside the baked cookiecutter
    """
    old_path = os.getcwd()
    try:
        os.chdir(str(bake.project_path))
        yield
    finally:
        os.chdir(old_path)


def wait_five_seconds(*args):
    time.sleep(5)
    return True