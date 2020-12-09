import github
import gitlab
import os
import pytest
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
def test_github_actions_ci_on_deployed_bake(cookies):
    bake = cookies.bake(extra_context={'github_actions_ci': 'Yes', 'project_slug': 'test-github-actions-cookiecutter-cpp-project'})
    with inside_bake(bake):
        # Push to Github
        subprocess.check_call("git remote add origin git@github.com:dokempf/test-github-actions-cookiecutter-cpp-project.git".split())
        subprocess.check_call("git push -f origin main".split())
        bake_sha1 = subprocess.run("git rev-parse HEAD".split(), capture_output=True).stdout.decode().strip()

        # Authenticate with the Github API
        gh = github.Github(os.getenv("GH_API_ACCESS_TOKEN"))

        # Find the workflow of the triggered Workflow - after giving it 2 seconds to properly initiate
        time.sleep(2)
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
    bake = cookies.bake(extra_context={'gitlab_ci': 'Yes', 'project_slug': 'test-gitlab-ci-cookiecutter-cpp-project'})
    with inside_bake(bake):
        # Push to Gitlab.com
        subprocess.check_call("git remote add origin git@gitlab.com:dokempf/test-gitlab-ci-cookiecutter-cpp-project.git".split())
        subprocess.check_call("git push -f origin main".split())
        bake_sha1 = subprocess.run("git rev-parse HEAD".split(), capture_output=True).stdout.decode().strip()

        # Authenticate with Gitlab API
        gl = gitlab.Gitlab('https://gitlab.com', private_token=os.getenv("GL_API_ACCESS_TOKEN"))
        gl.auth()

        # Find the correct Gitlab pipeline - after giving it 2 seconds to properly initiate
        time.sleep(2)
        pipeline = gl.projects.get('dokempf/test-gitlab-ci-cookiecutter-cpp-project').pipelines.list()[0]
        assert pipeline.sha == bake_sha1

        # Poll the pipeline status
        while pipeline.status != 'success':
            time.sleep(5)
            pipeline.refresh()
            if pipeline.status in ["failed", "cancelled", "skipped"]:
                pytest.fail("The Gitlab API reported Status '{}' while we were waiting for 'success'".format(status))
