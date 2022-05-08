import json
import jsonschema
import os
import pytest
import requests
import subprocess
from ruamel.yaml import YAML

from . import inside_bake


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


def build_cmake(target=None, ctest=False, install=False, **cmake_args):
    os.makedirs("build")
    os.chdir("build")
    optstr = " ".join("-D{}={}".format(k, v) for k, v in cmake_args.items())
    targetstr = "--target {}".format(target) if target is not None else ""
    subprocess.check_call("cmake {} ..".format(optstr).split())
    subprocess.check_call("cmake --build . {}".format(targetstr).split())
    if ctest:
        subprocess.check_call("ctest".split())
    if install:
        subprocess.check_call("cmake --build . --target install".split())


@pytest.mark.local
@pytest.mark.parametrize("externals", ("submodules", "vcpkg", "none"))
@pytest.mark.parametrize("header_only", ("Yes", "No"))
def test_ctest_run(cookies, externals, header_only):
    bake = cookies.bake(
        extra_context={
            'project_slug': 'test_project',
            'externals': externals,
            'header_only': header_only,
            'sonarcloud': 'No',
        }
    )
    check_bake(bake)
    with inside_bake(bake):
        build_cmake(ctest=True)


@pytest.mark.local
@pytest.mark.parametrize("header_only", ("Yes", "No"))
def test_cmake_installation(cookies, header_only):
    downstream_bake = cookies.bake(
        extra_context={
            'project_slug': 'downstream',
            'header_only': 'No',
            'sonarcloud': 'No',
        }
    )
    upstream_bake = cookies.bake(
        extra_context={
            'project_slug': 'upstream',
            'header_only': header_only,
            'sonarcloud': 'No',
        }
    )
    with inside_bake(upstream_bake):
        install_path = os.path.join(os.getcwd(), "inst")
        build_cmake(
            install=True,
            CMAKE_INSTALL_PREFIX=install_path
        )

    with inside_bake(downstream_bake):
        # Inject a find_package call
        with open("CMakeLists.txt", "r") as f:
            lines = f.readlines()
        with open("CMakeLists.txt", "w") as f:
            for line in lines:
                f.write(line)
                if line.startswith("project"):
                    f.write("find_package(upstream REQUIRED)\n")

        # Have the library depend on the upstream library
        with open("src/CMakeLists.txt", "a") as f:
            f.write("target_link_libraries(downstream PUBLIC upstream::upstream)\n")
        with open("src/downstream.cpp", "r") as f:
            lines = f.readlines()
        with open("src/downstream.cpp", "w") as f:
            f.write('#include "upstream/upstream.hpp"\n')
            for line in lines:
                f.write(line.replace("x + 1", "upstream::add_one(x)"))

        # Finally test the result
        build_cmake(ctest=True, CMAKE_PREFIX_PATH=install_path)


@pytest.mark.local
def test_with_remote(cookies):
    bake = cookies.bake(extra_context={'remote_url': 'https://github.com/dokempf/test-github-actions-cookiecutter-cpp-project.git'})
    check_bake(bake)
    assert bake.project.basename == 'test-github-actions-cookiecutter-cpp-project'
    with inside_bake(bake):
        assert len(subprocess.check_output("git remote -vv".split())) > 0


@pytest.mark.local
def test_readthedocs(cookies):
    bake = cookies.bake(
        extra_context={
            'readthedocs': 'Yes',
            'sonarcloud': 'No',
        }
    )
    check_bake(bake)
    with inside_bake(bake):
        build_cmake(target='sphinx-doc')
        assert os.path.exists(os.path.join(os.getcwd(), "doc", "sphinx", "index.html"))


@pytest.mark.local
def test_doxygen(cookies):
    bake = cookies.bake(
        extra_context={
            'doxygen': 'Yes',
            'sonarcloud': 'No',
        }
    )
    check_bake(bake)
    with inside_bake(bake):
        build_cmake(target='doxygen')
        assert os.path.exists(os.path.join(os.getcwd(), "doc", "html", "index.html"))


@pytest.mark.local
def test_github_actions_ci(cookies):
    bake = cookies.bake(
        extra_context={
            'remote_url': 'git@github.com:dokempf/test-github-actions-cookiecutter-cpp-project.git',
            'github_actions_ci': 'Yes',
            'python_bindings': 'Yes',
            'pypi_release': 'Yes',
            'sonarcloud': 'Yes',
        }
    )
    check_bake(bake)
    with inside_bake(bake):
        check_file_against_schemastore(".github/workflows/ci.yml", "https://json.schemastore.org/github-workflow")
        check_file_against_schemastore(".github/workflows/pypi.yml", "https://json.schemastore.org/github-workflow")
        check_file_against_schemastore(".github/workflows/sonarcloud.yml", "https://json.schemastore.org/github-workflow")


@pytest.mark.local
def test_gitlabci(cookies):
    bake = cookies.bake(
        extra_context={
            'gitlab_ci': 'Yes',
            'sonarcloud': 'No',
        }
    )
    check_bake(bake)
    with inside_bake(bake):
        check_file_against_schemastore(".gitlab-ci.yml", "https://gitlab.com/gitlab-org/gitlab/-/raw/master/app/assets/javascripts/editor/schema/ci.json")


@pytest.mark.local
@pytest.mark.parametrize("externals", ("submodules", "vcpkg", "none"))
def test_python(cookies, virtualenv, externals):
    bake = cookies.bake(
        extra_context={
            'project_slug': 'my-project',
            'python_bindings': 'Yes',
            'externals': externals,
            'sonarcloud': 'No',
        }
    )
    check_bake(bake)
    with inside_bake(bake):
        # Make sure that our Python package can be installed and imported
        subprocess.check_call([virtualenv.python, "-m", "pip", "install", "."])
        subprocess.check_call([virtualenv.python, "-c", "'import myproject'"])
        subprocess.check_call([virtualenv.python, "-m", "pip", "install", "-r", "requirements-dev.txt"])
        subprocess.check_call([virtualenv.python, "-m", "pytest"])


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
def test_sonarcloud_without_license(cookies):
    bake = cookies.bake(extra_context={'license': 'None', 'sonarcloud': 'Yes'})
    assert bake.exit_code != 0


@pytest.mark.local
def test_sonarcloud_without_github(cookies):
    bake = cookies.bake(extra_context={'github_actions_ci': 'No', 'sonarcloud': 'Yes'})
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
    bake = cookies.bake(
        extra_context={
            "github_actions_ci": "Yes",
            "gitlab_ci": "Yes",
            "remote_url": remote_url,
            "sonarcloud": "No",
        }
    )
    check_bake(bake)
