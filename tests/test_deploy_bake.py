import github
import gitlab
import os
import pytest
import pytools
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


@pytools.memoize
def remote_deploy_sha(c):
    bake = c.bake(extra_context={'github_actions_ci': 'Yes'})
    with inside_bake(bake):
        # Push to Github
        subprocess.check_call("git remote add origin git@github.com:dokempf/test-github-actions-cookiecutter-cpp-project.git".split())
        subprocess.check_call("git push -f origin main".split())
        # Push to Gitlab
        subprocess.check_call("git remote add gitlab git@github.com:dokempf/test-github-actions-cookiecutter-cpp-project.git".split())
        subprocess.check_call("git push -f gitlab main".split())
        # Wait for any integrations to trigger
        time.sleep(2)
        return subprocess.run("git rev-parse HEAD".split(), capture_output=True).stdout.decode().strip()


@pytest.mark.deploy
def test_github_actions_ci_on_deployed_bake(cookies):
    # Make sure that we have pushed a revision to our test repository
    bake_sha1 = remote_deploy_sha(cookies)

    # Authenticate with the Github API
    gh = github.Github(os.getenv("GH_API_ACCESS_TOKEN"))

    # Identify the correct workflow
    repo = gh.get_repo('dokempf/test-github-actions-cookiecutter-cpp-project')
    workflow = repo.get_workflow("ci.yml").get_runs()[0]
    assert workflow.head_sha == bake_sha1

    # Poll the workflow status
    while workflow.status != 'completed':
        # We poll at a relatively large interval to avoid running against the Github API
        # limitations in times of heavy development activities on the cookiecutter.
        time.sleep(30)
        workflow = repo.get_workflow("ci.yml").get_runs()[0]

    assert workflow.conclusion == 'success'


@pytest.mark.deploy
def test_gitlab_ci_on_deployed_bake(cookies):
    # Make sure that we have pushed a revision to our test repository
    bake_sha1 = remote_deploy_sha(cookies)

    # Authenticate with Gitlab API
    gl = gitlab.Gitlab('https://gitlab.com', private_token=os.getenv("GL_API_ACCESS_TOKEN"))
    gl.auth()

    # Find the correct Gitlab pipeline - after giving it 2 seconds to properly initiate
    pipeline = gl.projects.get('dokempf/test-gitlab-ci-cookiecutter-cpp-project').pipelines.list()[0]
    assert pipeline.sha == bake_sha1

    # Poll the pipeline status
    while pipeline.status != 'success':
        time.sleep(5)
        pipeline.refresh()
        if pipeline.status in ["failed", "cancelled", "skipped"]:
            pytest.fail("The Gitlab API reported Status '{}' while we were waiting for 'success'".format(status))


@pytest.mark.deploy
def test_readthedocs_deploy(cookies):
    # Make sure that we have pushed a revision to our test repository
    bake_sha1 = remote_deploy_sha(cookies)

    def rtd_api_request(endpoint):
        response = requests.get(
            'https://readthedocs.org/api/v3/projects/test-github-actions-cookiecutter-cpp-project/{}'.format(endpoint),
            headers={'Authorization': 'token {}'.format(os.getenv('RTD_API_ACCESS_TOKEN'))}
        )
        return response.json()

    # Check that the build has the correct commit
    last_build_id = rtd_api_request("versions/latest/builds")["results"][0]["id"]
    build = rtd_api_request('builds/{}'.format(last_build_id))
    assert build["commit"] == bake_sha1

    # Wait until the build has finished
    while build['state']['code'] != 'finished':
        time.sleep(5)
        build = rtd_api_request('builds/{}'.format(last_build_id))

    assert build['success']
