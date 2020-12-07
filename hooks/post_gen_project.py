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

# Run 'git init' on the generated project
subprocess.call("git init".split())

# Add submodules depending on features
def add_submodule(url, location, branch=None):
    command = ["git", "submodule", "add"]
    if branch is not None:
        command = command + ["-b", branch]
    command = command + [url, location]
    ret = subprocess.call(command)
    if ret != 0:
        sys.exit(ret)

add_submodule("https://github.com/catchorg/Catch2.git", "ext/Catch2", branch="v2.x")
if "{{ cookiecutter.python_bindings }}" == "Yes":
    add_submodule("https://github.com/pybind/pybind11.git", "ext/pybind11", branch="stable")

# Finalize by making an initial git commit
subprocess.call("git add *".split())
subprocess.call(["git", "commit", "-m", "Initial Commit"])

# Print a message about success
print("The project {{ cookiecutter.project_slug }} was successfully generated!")
if os.path.exists("TODO.md"):
    print("A TODO list for you to finalize the generation process was also generated, see TODO.md")
