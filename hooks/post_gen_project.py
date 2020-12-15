# This script executes after the project is generated from your cookiecutter.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
#
# An example of a post-hook would be to remove parts of the project
# directory tree based on some configuration values.

import os
import subprocess
import sys
from cookiecutter.utils import rmtree


class GitRepository(object):
    """ A context for the setup of a Git repository """
    def __enter__(self):
        # Initialize the git repository
        subprocess.check_call("git init".split())
        subprocess.check_call("git checkout -b main".split())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Finalize by making an initial git commit
        subprocess.check_call("git add *".split())
        subprocess.check_call(["git", "commit", "-m", "Initial Commit"])
        {% if cookiecutter.remote_url != 'None' %}
        subprocess.check_call("git remote add origin {{ cookiecutter.remote_url }}".split())
        {% endif %}

    def add_submodule(self, url, location, branch=None, tag=None):
        command = ["git", "submodule", "add"]
        if branch is not None:
            command = command + ["-b", branch]
        command = command + [url, location]
        subprocess.check_call(command)
        if tag is not None:
            subprocess.check_call(["git", "checkout", tag], cwd=os.path.join(os.getcwd(), *os.path.split(location)))


# Optionally remove files whose existence is tied to disabled features
def conditional_remove(condition, path):
    if condition:
        if os.path.isfile(path):
            os.remove(path)
        else:
            rmtree(path)


conditional_remove(True, "ext/.keep")
conditional_remove("{{ cookiecutter.use_submodules }}" == "No", "ext")
conditional_remove("{{ cookiecutter.license }}" == "None", "LICENSE.md")
conditional_remove("{{ cookiecutter.gitlab_ci }}" == "No", ".gitlab-ci.yml")
conditional_remove("{{ cookiecutter.readthedocs }}" == "No", ".readthedocs.yml")
conditional_remove("{{ cookiecutter.readthedocs }}" == "No", "doc/conf.py")
conditional_remove("{{ cookiecutter.readthedocs }}" == "No", "doc/index.rst")
conditional_remove("{{ cookiecutter.readthedocs }}" == "No", "doc/requirements-rtd.txt")
conditional_remove("{{ cookiecutter.doxygen }}" == "No" and "{{ cookiecutter.readthedocs }}" == "No", "doc")
conditional_remove("{{ cookiecutter.python_bindings }}" == "No", "setup.py")
conditional_remove("{{ cookiecutter.python_bindings }}" == "No", "python")
conditional_remove("{{ cookiecutter.pypi_release }}" != "Yes", ".github/workflows/pypi.yml")
conditional_remove("{{ cookiecutter.github_actions_ci }}" == "No", ".github")
conditional_remove(os.stat("TODO.md").st_size == 0, "TODO.md")


# Set up a Git repository with submodules
with GitRepository() as repo:
{% if cookiecutter.use_submodules == "Yes" %}
    repo.add_submodule("https://github.com/catchorg/Catch2.git", "ext/Catch2", tag="v2.13.3")
    if "{{ cookiecutter.python_bindings }}" == "Yes":
        repo.add_submodule("https://github.com/pybind/pybind11.git", "ext/pybind11", tag="v2.6.1")
{% else %}
    pass
{% endif %}


# Print a message about success
print("The project {{ cookiecutter.project_slug }} was successfully generated!")
if os.path.exists("TODO.md"):
    print("A TODO list for you to finalize the generation process was also generated, see TODO.md")
