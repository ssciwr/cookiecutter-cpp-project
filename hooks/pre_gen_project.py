# This script executes before the project is generated from your cookiecutter.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
#
# An example of a pre-hook would be to validate the provided input for a
# user configuration value and exit with an error upon failure.

import sys


def fail_if(condition, message):
    if condition:
        sys.stderr.write(message)
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
    "{{ cookiecutter.sonarcloud }}" == "Yes" and "{{ cookiecutter.license }}" == "None",
    "Code quality analysis from sonarcloud.io requires an open source license for your project"
)

fail_if(
    "{{ cookiecutter.sonarcloud }}" == "Yes" and "{{ cookiecutter.github_actions_ci }}" == "No",
    "Code quality analysis from sonarcloud.io is currently only supported in combination with Github Actions CI"
)

fail_if(
    "{{ cookiecutter.sonarcloud }}" == "Yes" and "github.com" not in "{{ cookiecutter.remote_url }}",
    "Code quality analysis from sonarcloud.io is currently only supported in combination with a Github remote repository"
)
