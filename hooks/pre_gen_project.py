# This script executes before the project is generated from your cookiecutter.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
#
# An example of a pre-hook would be to validate the provided input for a
# user configuration value and exit with an error upon failure.

import cookiecutter
import sys


# Native booleans require 2.2; descriptive choice labels require 2.2.3.
parts = tuple(int(part) for part in cookiecutter.__version__.split(".")[:3])
if parts < (2, 2, 3):
    sys.stderr.write("This template requires cookiecutter >= 2.2.3\n")
    sys.exit(1)


def fail_if(condition, message):
    if condition:
        sys.stderr.write(message + "\n")
        sys.exit(1)


fail_if(
    not {{ cookiecutter.doxygen }} and {{ cookiecutter.readthedocs }},
    "Read the Docs requires Doxygen in this template; set doxygen to true"
)

fail_if(
    {{ cookiecutter.pypi_release }} and "{{ cookiecutter.python_bindings }}" == "None",
    "Can't do PyPI release without building Python bindings"
)

fail_if(
    {{ cookiecutter.pypi_release }} and not {{ cookiecutter.github_actions_ci }},
    "Automatic PyPI releases are currently only supported in combination with Github Actions CI"
)

fail_if(
    {{ cookiecutter.codecovio }} and "{{ cookiecutter.license }}" == "None",
    "Coverage reports for codecov.io require an open source license for your project"
)

fail_if(
    {{ cookiecutter.codecovio }} and not {{ cookiecutter.github_actions_ci }},
    "Coverage reports for codecov.io are only supported for Github Actions CI"
)
