import json
import jsonschema
import os
import pytest
import requests
import subprocess
from ruamel.yaml import YAML
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


def check_file_against_schemastore(filename, schema_url):
    """
    Validate a YAML file against a JSON schema that is downloaded from the web
    """
    schema = json.loads(requests.get(schema_url).text)
    yaml = YAML(typ='safe')
    with open(filename) as f:
        config = yaml.load(f)
    try:
        jsonschema.validate(config, schema)
    except jsonschema.ValidationError:
        pytest.fail("{} validation check failed!".format(filename))


def check_bake(bake):
    if bake.exception:
        raise bake.exception
    assert bake.exit_code == 0
    assert bake.project.isdir()


@pytest.mark.local
def test_project_tree(cookies):
    bake = cookies.bake(extra_context={'project_slug': 'test_project'})
    check_bake(bake)
    with inside_bake(bake):
        os.makedirs("build")
        os.chdir("build")
        subprocess.check_call("cmake ..".split())
        subprocess.check_call("cmake --build .".split())
        subprocess.check_call("ctest".split())


@pytest.mark.local
def test_readthedocs(cookies):
    bake = cookies.bake(extra_context={'readthedocs': 'Yes'})
    check_bake(bake)
    with inside_bake(bake):
        os.makedirs("build")
        os.chdir("build")
        subprocess.check_call("cmake ..".split())
        subprocess.check_call("cmake --build . --target sphinx-doc".split())
        assert os.path.exists(os.path.join(os.getcwd(), "doc", "sphinx", "index.html"))


@pytest.mark.local
def test_doxygen(cookies):
    bake = cookies.bake(extra_context={'doxygen': 'Yes'})
    check_bake(bake)
    with inside_bake(bake):
        os.makedirs("build")
        os.chdir("build")
        subprocess.check_call("cmake ..".split())
        subprocess.check_call("cmake --build . --target doxygen".split())
        assert os.path.exists(os.path.join(os.getcwd(), "doc", "html", "index.html"))


@pytest.mark.local
def test_github_actions_ci(cookies):
    bake = cookies.bake(extra_context={'github_actions_ci': 'Yes', 'python_bindings': 'Yes', 'pypi_release': 'Yes'})
    check_bake(bake)
    with inside_bake(bake):
        check_file_against_schemastore(".github/workflows/ci.yml", "https://json.schemastore.org/github-workflow")
        check_file_against_schemastore(".github/workflows/pypi.yml", "https://json.schemastore.org/github-workflow")


@pytest.mark.local
def test_gitlabci(cookies):
    bake = cookies.bake(extra_context={'gitlab_ci': 'Yes'})
    check_bake(bake)
    with inside_bake(bake):
        check_file_against_schemastore(".gitlab-ci.yml", "https://json.schemastore.org/gitlab-ci")


@pytest.mark.local
def test_travisci(cookies):
    bake = cookies.bake(extra_context={'travis_ci': 'Yes'})
    check_bake(bake)
    with inside_bake(bake):
        check_file_against_schemastore(".travis.yml", "https://json.schemastore.org/travis")


@pytest.mark.local
def test_python(cookies, virtualenv):
    bake = cookies.bake(extra_context={'project_slug': 'my-project', 'python_bindings': 'Yes'})
    check_bake(bake)
    with inside_bake(bake):
        # Make sure that our Python package can be installed and imported
        subprocess.check_call([virtualenv.python, "-m", "pip", "install", "."])
        subprocess.check_call([virtualenv.python, "-c", "'import myproject'"])
        subprocess.check_call([virtualenv.python, "-m", "pip", "install", "pytest"])
        subprocess.check_call([virtualenv.python, "-m", "pytest"], cwd=os.path.join(os.getcwd(), "python"))


@pytest.mark.local
def test_pypi_without_python(cookies):
    bake = cookies.bake(extra_context={'python_bindings': 'No', 'pypi_release': 'Yes'})
    assert bake.exit_code != 0


@pytest.mark.local
def test_pypi_without_github(cookies):
    bake = cookies.bake(extra_context={'github_actions_ci': 'No', 'pypi_release': 'Yes', 'python_bindings': 'Yes'})
    assert bake.exit_code != 0
