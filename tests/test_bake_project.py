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
@pytest.mark.parametrize("submodules", ("Yes", "No"))
def test_ctest_run(cookies, submodules):
    bake = cookies.bake(
        extra_context={
            'project_slug': 'test_project',
            'use_submodules': submodules,
        }
    )
    check_bake(bake)
    with inside_bake(bake):
        os.makedirs("build")
        os.chdir("build")
        subprocess.check_call("cmake ..".split())
        subprocess.check_call("cmake --build .".split())
        subprocess.check_call("ctest".split())


@pytest.mark.local
def test_with_remote(cookies):
    bake = cookies.bake(extra_context={'remote_url': 'https://github.com/dokempf/test-github-actions-cookiecutter-cpp-project.git'})
    check_bake(bake)
    assert bake.project.basename == 'test-github-actions-cookiecutter-cpp-project'
    with inside_bake(bake):
        assert len(subprocess.check_output("git remote -vv".split())) > 0


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
@pytest.mark.parametrize("submodules", ("Yes", "No"))
def test_python(cookies, virtualenv, submodules):
    bake = cookies.bake(
        extra_context={
            'project_slug': 'my-project',
            'python_bindings': 'Yes',
            'submodules': submodules,
        }
    )
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


@pytest.mark.local
def test_codecov_without_license(cookies):
    bake = cookies.bake(extra_context={'license': 'None', 'codecovio': 'Yes'})
    assert bake.exit_code != 0


@pytest.mark.local
@pytest.mark.parametrize(
    "remote_url",
    [
        "git@github.com:dokempf/test-github-actions-cookiecutter-cpp-project.git",
        "https://github.com/dokempf/test-github-actions-cookiecutter-cpp-project.git",
        "git@gitlab.com:dokempf/test-gitlab-ci-cookiecutter-cpp-project.git",
        "https://gitlab.com/dokempf/test-gitlab-ci-cookiecutter-cpp-project.git",
        "ssh://git@gitlab.dune-project.org:22022/dominic/test-gitlab-ci-cookiecutter-cpp-project.git",
        "https://gitlab.dune-project.org/dominic/test-gitlab-ci-cookiecutter-cpp-project.git"
    ])
def test_remote_urls(cookies, remote_url):
    bake = cookies.bake(extra_context={"github_actions_ci": "Yes", "gitlab_ci": "Yes", "remote_url": remote_url})
    check_bake(bake)
