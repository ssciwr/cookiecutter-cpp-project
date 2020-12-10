import github
import gitlab
import os
import re
import pytest
import requests
import subprocess
import time
from contextlib import contextmanager
from packaging import version


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


@pytest.mark.deploy
def test_push_remote(cookies):
    # We configure one project that has all implemented integrations enabled.
    bake = cookies.bake(
        extra_context={
            'project_name': 'My C++ Project',
            'project_slug': 'test-github-actions-cookiecutter-cpp-project',
            'github_actions_ci': 'Yes',
            'gitlab_ci': 'Yes',
            'travis_ci': 'Yes',
            'readthedocs': 'Yes',
            'python_bindings': 'Yes',
            'pypi_release': 'Yes',
        }
    )
    with inside_bake(bake):
        # Push to Github
        subprocess.check_call("git remote add origin git@github.com:dokempf/test-github-actions-cookiecutter-cpp-project.git".split())
        subprocess.check_call("git push -f origin main".split())
        # Push to Gitlab
        subprocess.check_call("git remote add gitlab git@gitlab.com:dokempf/test-gitlab-ci-cookiecutter-cpp-project.git".split())
        subprocess.check_call("git push -f gitlab main".split())


@pytest.mark.integrations
def test_github_actions_ci_on_deployed_bake():
    # Authenticate with the Github API
    gh = github.Github(os.getenv("GH_API_ACCESS_TOKEN"))

    # Identify the correct workflow
    repo = gh.get_repo('dokempf/test-github-actions-cookiecutter-cpp-project')
    branch = repo.get_branch('main')
    workflow = repo.get_workflow("ci.yml").get_runs()[0]
    assert workflow.head_sha == branch.commit.sha

    # Poll the workflow status
    while workflow.status != 'completed':
        # We poll at a relatively large interval to avoid running against the Github API
        # limitations in times of heavy development activities on the cookiecutter.
        time.sleep(30)
        workflow = repo.get_workflow("ci.yml").get_runs()[0]

    assert workflow.conclusion == 'success'


@pytest.mark.integrations
def test_gitlab_ci_on_deployed_bake():
    # Authenticate with Gitlab API
    gl = gitlab.Gitlab('https://gitlab.com', private_token=os.getenv("GL_API_ACCESS_TOKEN"))
    gl.auth()

    # Find the correct Gitlab pipeline - after giving it 2 seconds to properly initiate
    project = gl.projects.get('dokempf/test-gitlab-ci-cookiecutter-cpp-project')
    pipeline = project.pipelines.list()[0]
    branch = project.branches.get('main')
    assert pipeline.sha == branch.commit['id']

    # Poll the pipeline status
    while pipeline.status != 'success':
        time.sleep(5)
        pipeline.refresh()
        if pipeline.status in ["failed", "cancelled", "skipped"]:
            pytest.fail("The Gitlab API reported Status '{}' while we were waiting for 'success'".format(status))


@pytest.mark.integrations
def test_readthedocs_deploy():
    # Authenticate with the Github API to get the upstream commit
    gh = github.Github(os.getenv("GH_API_ACCESS_TOKEN"))
    repo = gh.get_repo('dokempf/test-github-actions-cookiecutter-cpp-project')
    sha = repo.get_branch('main').commit.sha

    def rtd_api_request(endpoint):
        response = requests.get(
            'https://readthedocs.org/api/v3/projects/test-github-actions-cookiecutter-cpp-project/{}'.format(endpoint),
            headers={'Authorization': 'token {}'.format(os.getenv('RTD_API_ACCESS_TOKEN'))}
        )
        return response.json()

    # Check that the build has the correct commit
    last_build_id = rtd_api_request("versions/latest/builds")["results"][0]["id"]
    build = rtd_api_request('builds/{}'.format(last_build_id))

    # Wait until the build has finished
    while build['state']['code'] != 'finished':
        time.sleep(5)
        build = rtd_api_request('builds/{}'.format(last_build_id))

    assert build['success']
    assert build["commit"] == sha


@pytest.mark.integrations
def test_pypi_deploy(virtualenv):
    # Find out the current version of the PyPI package
    def upstream_version(url):
        response = requests.get(url)
        if response.status_code == 200:
            return version.parse(response.json()['info']['version'])
        else:
            return version.parse('0.0.0')

    # Construct a version, by finding the maximum version across Github, PyPI and TestPyPI and increasing that
    gh = github.Github(os.getenv("GH_API_ACCESS_TOKEN"))
    repo = gh.get_repo('dokempf/test-github-actions-cookiecutter-cpp-project')
    current_version = max([
        upstream_version('https://pypi.org/pypi/testgithubactionscookiecuttercppproject/json'),
        upstream_version('https://test.pypi.org/pypi/testgithubactionscookiecuttercppproject/json'),
        version.parse(repo.get_latest_release().title[1:])
    ])
    next_version = version.Version('{}.{}.{}'.format(current_version.major, current_version.minor, current_version.micro + 1))

    # Modify the version in setup.py and commit the change
    subprocess.check_call("git clone git@github.com:dokempf/test-github-actions-cookiecutter-cpp-project.git".split())
    os.chdir("test-github-actions-cookiecutter-cpp-project")
    with open("setup.py", "r") as source:
        lines = source.readlines()
    with open("setup.py", "w") as source:
        for line in lines:
            source.write(re.sub(r'version=.*$', 'version="{}",'.format(str(next_version)), line))
    subprocess.check_call("git add setup.py".split())
    subprocess.check_call(["git", "commit", "-m", "Bump version in setup.py"])
    subprocess.check_call("git push -f origin main:pypi_release".split())
    time.sleep(2)

    # Create the release - this will trigger the PyPI release workflow
    repo.create_git_release(
        'v{}'.format(str(next_version)),
        'v{}'.format(str(next_version)),
        "Test Release",
        target_commitish='pypi_release'
    )
    time.sleep(2)

    # Identify the PyPI release workflow
    branch = repo.get_branch('pypi_release')
    workflow = repo.get_workflow("pypi.yml").get_runs()[0]
    assert workflow.head_sha == branch.commit.sha

    # Poll the workflow status
    while workflow.status != 'completed':
        # We poll at a relatively large interval to avoid running against the Github API
        # limitations in times of heavy development activities on the cookiecutter.
        time.sleep(30)
        workflow = repo.get_workflow("pypi.yml").get_runs()[0]

    assert workflow.conclusion == 'success'

    # Install the package into a virtualenv and load it
    time.sleep(2)
    virtualenv.install_package('testgithubactionscookiecuttercppproject=={}'.format(str(next_version)))
    subprocess.check_call([virtualenv.python, "-c", "'import testgithubactionscookiecuttercppproject'"])
