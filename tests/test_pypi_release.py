import github
import os
import re
import pytest
import requests
import subprocess
import time
import tomlkit

from packaging import version


@pytest.mark.pypi
@pytest.mark.timeout(1800)
def test_pypi_deploy():
    # Find out the current version of the PyPI package
    def upstream_version(url):
        response = requests.get(url)
        if response.status_code == 200:
            return version.parse(response.json()['info']['version'])
        else:
            return version.parse('0.0.0')

    # Construct a version, by finding the maximum version across Github, PyPI and TestPyPI and increasing that
    gh = github.Github(os.getenv("GH_API_ACCESS_TOKEN"))
    repo = gh.get_repo('dokempf/test-gha-cookiecutter')

    # Modify the version in pyproject.toml and commit the change
    subprocess.check_call("git clone git@github.com:dokempf/test-gha-cookiecutter.git".split())
    os.chdir("test-gha-cookiecutter")
    subprocess.check_call(["git", "switch", "--track", "origin/pypi_release"])

    # Parse the pyproject.toml file to get the current version on the branch
    with open("pyproject.toml", "r") as f:
        data = tomlkit.parse(f.read())
    branch_version = version.parse(data["project"]["version"])

    # Identify the maximum version across PyPI, TestPyPI, Github and the branch and increase that by one patch version
    current_version = max([
        upstream_version('https://pypi.org/pypi/testghacookiecutter/json'),
        upstream_version('https://test.pypi.org/pypi/testghacookiecutter/json'),
        version.parse(repo.get_latest_release().title[1:]),
        branch_version
    ])

    # Increase the version by one
    next_version = version.Version('{}.{}.{}'.format(current_version.major, current_version.minor, current_version.micro + 1))

    # Update the version in pyproject.toml
    data["project"]["version"] = str(next_version)
    with open("pyproject.toml", "w") as f:
        f.write(tomlkit.dumps(data))

    # Commit the change and push it to the remote branch
    subprocess.check_call("git add pyproject.toml".split())
    subprocess.check_call(["git", "commit", "-m", "Bump version in pyproject.toml"])
    subprocess.check_call("git push -f origin pypi_release".split())
    time.sleep(2)

    # Create the release tag - this will trigger the PyPI release workflow
    branch = repo.get_branch("pypi_release")

    repo.create_git_ref(
        ref=f"refs/tags/v{next_version}",
        sha=branch.commit.sha,
    )
    time.sleep(2)

    # Identify the PyPI release workflow
    workflow = repo.get_workflow("pypi.yml").get_runs()[0]
    assert workflow.head_sha == branch.commit.sha

    # Poll the workflow status
    while workflow.status != 'completed':
        # We poll at a relatively large interval to avoid running against the Github API
        # limitations in times of heavy development activities on the cookiecutter.
        time.sleep(30)
        workflow = repo.get_workflow("pypi.yml").get_runs()[0]

    assert workflow.conclusion == 'success'
