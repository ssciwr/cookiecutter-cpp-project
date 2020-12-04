from contextlib import contextmanager

import os
import requests
import subprocess


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


def test_project_tree(cookies):
    bake = cookies.bake(extra_context={'project_slug': 'test_project'})
    assert bake.exit_code == 0
    assert bake.exception is None
    assert bake.project.basename == 'test_project'
    assert bake.project.isdir()

    with inside_bake(bake):
        os.makedirs("build")
        os.chdir("build")
        assert subprocess.call("cmake ..".split()) == 0
        assert subprocess.call("cmake --build .".split()) == 0
        assert subprocess.call("ctest".split()) == 0


def test_doxygen(cookies):
    bake = cookies.bake(extra_context={'doxygen': 'Yes'})
    with inside_bake(bake):
        os.makedirs("build")
        os.chdir("build")
        assert subprocess.call("cmake ..".split()) == 0
        assert subprocess.call("cmake --build . --target doxygen".split()) == 0
        assert os.path.exists(os.path.join(os.getcwd(), "doc", "html", "index.html"))


def test_gitlabci(cookies):
    bake = cookies.bake(extra_context={'gitlab_ci': 'Yes'})
    with inside_bake(bake):
        with open(".gitlab-ci.yml") as f:
            r = requests.post("https://gitlab.com/api/v4/ci/lint", json={'content': f.read()})
        assert r.status_code == requests.codes['OK']
        assert r.json()["status"] == "valid"
