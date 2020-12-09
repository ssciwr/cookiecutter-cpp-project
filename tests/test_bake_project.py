from contextlib import contextmanager

import gitlab
import json
import jsonschema
import os
import pytest
import requests
import subprocess
import time
from ruamel.yaml import YAML


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


def test_project_tree(cookies):
    bake = cookies.bake(extra_context={'project_slug': 'test_project'})
    assert bake.exit_code == 0
    assert bake.exception is None
    assert bake.project.basename == 'test_project'
    assert bake.project.isdir()

    with inside_bake(bake):
        os.makedirs("build")
        os.chdir("build")
        subprocess.check_call("cmake ..".split())
        subprocess.check_call("cmake --build .".split())
        subprocess.check_call("ctest".split())


def test_doxygen(cookies):
    bake = cookies.bake(extra_context={'doxygen': 'Yes'})
    with inside_bake(bake):
        os.makedirs("build")
        os.chdir("build")
        subprocess.check_call("cmake ..".split())
        subprocess.check_call("cmake --build . --target doxygen".split())
        assert os.path.exists(os.path.join(os.getcwd(), "doc", "html", "index.html"))


def test_github_actions_ci(cookies):
    bake = cookies.bake(extra_context={'github_actions_ci': 'Yes', 'python_bindings': 'Yes', 'pypi_release': 'Yes'})
    with inside_bake(bake):
        check_file_against_schemastore(".github/workflows/ci.yml", "https://json.schemastore.org/github-workflow")
        check_file_against_schemastore(".github/workflows/pypi.yml", "https://json.schemastore.org/github-workflow")


def test_gitlabci(cookies):
    bake = cookies.bake(extra_context={'gitlab_ci': 'Yes'})
    with inside_bake(bake):
        check_file_against_schemastore(".gitlab-ci.yml", "https://json.schemastore.org/gitlab-ci")


def test_travisci(cookies):
    bake = cookies.bake(extra_context={'travis_ci': 'Yes'})
    with inside_bake(bake):
        check_file_against_schemastore(".travis.yml", "https://json.schemastore.org/travis")


def test_python(cookies, virtualenv):
    bake = cookies.bake(extra_context={'project_slug': 'my-project', 'python_bindings': 'Yes'})
    with inside_bake(bake):
        # Make sure that our Python package can be installed and imported
        subprocess.check_call([virtualenv.python, "-m", "pip", "install", "."])
        subprocess.check_call([virtualenv.python, "-c", "'import myproject'"])
        subprocess.check_call([virtualenv.python, "-m", "pip", "install", "pytest"])
        subprocess.check_call([virtualenv.python, "-m", "pytest"], cwd=os.path.join(os.getcwd(), "python"))


def test_pypi_without_python(cookies):
    bake = cookies.bake(extra_context={'python_bindings': 'No', 'pypi_release': 'Yes'})
    assert bake.exit_code != 0


def test_pypi_without_github(cookies):
    bake = cookies.bake(extra_context={'github_actions_ci': 'No', 'pypi_release': 'Yes', 'python_bindings': 'Yes'})
    assert bake.exit_code != 0


def test_github_actions_ci_on_deployed_bake(cookies):
    bake = cookies.bake(extra_context={'github_actions_ci': 'Yes', 'project_slug': 'test-github-actions-cookiecutter-cpp-project'})
    with inside_bake(bake):
        # Push to Github
        subprocess.check_call("git remote add origin git@github.com:dokempf/test-github-actions-cookiecutter-cpp-project.git".split())
        subprocess.check_call("git push -f origin main".split())

        # Find the Workflow ID of the triggered Workflow - after giving it 2 seconds to properly initiate
        time.sleep(2)
        bake_sha1 = subprocess.run("git rev-parse HEAD".split(), capture_output=True).stdout.decode()
        req = requests.get(
            "https://api.github.com/repos/dokempf/test-github-actions-cookiecutter-cpp-project/actions/workflows/ci.yml/runs",
            headers={'Authorization': os.getenv("GH_API_ACCESS_TOKEN")}
        )
        workflow_id = None
        for workflow in json.loads(req.text)['workflow_runs']:
            if workflow['head_sha'] == bake_sha1.strip():
                workflow_id = workflow['id']
        assert workflow_id is not None

        # Poll the Github API if the Workflow completed
        def check_complete():
            req = requests.get(
                "https://api.github.com/repos/dokempf/test-github-actions-cookiecutter-cpp-project/actions/runs/{}".format(workflow_id),
                headers={'Authorization': os.getenv("GH_API_ACCESS_TOKEN")}
            )
            status = json.loads(req.text)["status"]
            return status == 'completed'

        while not check_complete():
            # We poll at a relatively large interval to avoid running against the Github API
            # limitations in times of heavy development activities on the cookiecutter.
            time.sleep(30)

        # We require the CI run to be successful!
        req = requests.get(
            "https://api.github.com/repos/dokempf/test-github-actions-cookiecutter-cpp-project/actions/runs/{}".format(workflow_id),
            headers={'Authorization': os.getenv("GH_API_ACCESS_TOKEN")}
        )
        assert json.loads(req.text)["conclusion"] == 'success'


def test_gitlab_ci_on_deployed_bake(cookies):
    bake = cookies.bake(extra_context={'gitlab_ci': 'Yes', 'project_slug': 'test-gitlab-ci-cookiecutter-cpp-project'})
    with inside_bake(bake):
        # Push to Gitlab.com
        subprocess.check_call("git remote add origin git@gitlab.com:dokempf/test-gitlab-ci-cookiecutter-cpp-project.git".split())
        subprocess.check_call("git push -f origin main".split())

        # Authenticate with Gitlab API
        gl = gitlab.Gitlab('https://gitlab.com', private_token=os.getenv("GL_API_ACCESS_TOKEN"))
        gl.auth()

        # Find the correct Gitlab pipeline - after giving it 2 seconds to properly initiate
        time.sleep(2)
        bake_sha1 = subprocess.run("git rev-parse HEAD".split(), capture_output=True).stdout.decode().strip()
        pipeline = None
        for pl in gl.projects.get('dokempf/test-gitlab-ci-cookiecutter-cpp-project').pipelines.list():
            if pl.sha == bake_sha1:
                pipeline = pl
        assert pipeline is not None

        while pipeline.status == 'success':
            # We poll at a relatively large interval to avoid running against the Github API
            # limitations in times of heavy development activities on the cookiecutter.
            time.sleep(30)
            pipeline.refresh()
            if pipeline.status in ["failed", "cancelled", "skipped"]:
                pytest.fail("The Gitlab API reported Status '{}' while we were waiting for 'success'".format(status))
