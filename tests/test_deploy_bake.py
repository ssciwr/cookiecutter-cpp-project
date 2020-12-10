import github
import gitlab
import os
import pytest
import requests
import subprocess
import time
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


@pytest.mark.deploy
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


@pytest.mark.deploy
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
