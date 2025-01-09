# This script executes before the project is generated from your cookiecutter.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
#
# An example of a pre-hook would be to validate the provided input for a
# user configuration value and exit with an error upon failure.

import cookiecutter
import sys


# Ensure that the version of cookiecutter is >= 2.1. Unfortunately, we cannot
# use the packaging library here, because we cannot install additional dependencies
# and cookiecutter did not depend on it pre-v2
parts = cookiecutter.__version__.split(".")
if int(parts[0]) < 2 or (int(parts[0]) == 2  and int(parts[1]) < 1):
    sys.stderr.write("This template requires cookiecutter >= 2.1")
    sys.exit(1)


def fail_if(condition, message):
    if condition:
        sys.stderr.write(message + "\n")
        sys.exit(1)


fail_if(
    "{{ cookiecutter.pypi_release }}" != "No" and "{{ cookiecutter.python_bindings }}" == "No",
    "Can't do PyPI release without building Python bindings"
)

fail_if(
    "{{ cookiecutter.pypi_release }}" != "No" and "{{ cookiecutter.github_actions_ci }}" == "No",
    "Automatic PyPI releases are currently only supported in combination with Github Actions CI"
)

fail_if(
    "{{ cookiecutter.codecovio }}" == "Yes" and "{{ cookiecutter.license }}" == "None",
    "Coverage reports for codecov.io require an open source license for your project"
)

fail_if(
    "{{ cookiecutter.codecovio }}" == "Yes" and "{{ cookiecutter.github_actions_ci }}" == "No",
    "Coverage reports for codecov.io are only supported for Github Actions CI"
)
