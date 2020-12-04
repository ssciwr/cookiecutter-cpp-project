# This script executes after the project is generated from your cookiecutter.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
#
# An example of a post-hook would be to remove parts of the project
# directory tree based on some configuration values.

import os
import subprocess

# Optionally remove files whose existence is tied to disabled features

if "{{ cookiecutter.license }}" == "None":
    os.remove("LICENSE.md")

# Run 'git init' on the generated project
subprocess.call("git init".split())

# Add submodules depending on features
subprocess.call("git submodule add -b v2.x https://github.com/catchorg/Catch2.git ext/Catch2".split())

# Finalize by making an initial git commit
subprocess.call("git add *".split())
subprocess.call(["git", "commit", "-m" "Initial Commit"])
