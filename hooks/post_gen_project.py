# This script executes after the project is generated from your cookiecutter.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
#
# An example of a post-hook would be to remove parts of the project
# directory tree based on some configuration values.

import os
import shutil
import subprocess
import sys
from contextlib import contextmanager


class GitRepository(object):
    """ A context for the setup of a Git repository """
    def __enter__(self):
        # Initialize the git repository
        subprocess.check_call("git init".split())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Finalize by making an initial git commit
        subprocess.check_call("git add *".split())
        subprocess.check_call(["git", "commit", "-m", "Initial Commit"])

    def add_submodule(self, url, location, branch=None, tag=None):
        command = ["git", "submodule", "add"]
        if branch is not None:
            command = command + ["-b", branch]
        command = command + [url, location]
        subprocess.check_call(command)
        if tag is not None:
            subprocess.check_call(["git", "checkout", tag], cwd=os.path.join(os.getcwd(), *os.path.split(location)))


# Optionally remove files whose existence is tied to disabled features
if "{{ cookiecutter.license }}" == "None":
    os.remove("LICENSE.md")

if "{{ cookiecutter.github_actions_ci }}" == "No":
    os.remove(".github/workflows/ci.yml")

if "{{ cookiecutter.gitlab_ci }}" == "No":
    os.remove(".gitlab-ci.yml")

if "{{ cookiecutter.travis_ci }}" == "No":
    os.remove(".travis.yml")

if "{{ cookiecutter.doxygen }}" == "No":
    os.rmdir("doc")

if "{{ cookiecutter.python_bindings }}" == "No":
    os.remove("setup.py")
    shutil.rmtree("python")

# If the TODO.md file is empty, we remove it
if os.stat("TODO.md").st_size == 0:
    os.remove("TODO.md")


# Set up a Git repository with submodules
with GitRepository() as repo:
    repo.add_submodule("https://github.com/catchorg/Catch2.git", "ext/Catch2", tag="v2.13.3")
    if "{{ cookiecutter.python_bindings }}" == "Yes":
        repo.add_submodule("https://github.com/pybind/pybind11.git", "ext/pybind11", tag="v2.6.1")


# Print a message about success
print("The project {{ cookiecutter.project_slug }} was successfully generated!")
if os.path.exists("TODO.md"):
    print("A TODO list for you to finalize the generation process was also generated, see TODO.md")
