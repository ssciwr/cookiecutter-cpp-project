# This script executes before the project is generated from your cookiecutter.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
#
# An example of a pre-hook would be to validate the provided input for a
# user configuration value and exit with an error upon failure.

import sys

if "{{ cookiecutter.pypi_release }}" != "No" and "{{ cookiecutter.python_bindings }}" == "No":
    sys.stderr.write("Can't do PyPI release without building Python bindings")
    sys.exit(1)

if "{{ cookiecutter.pypi_release }}" != "No" and "{{ cookiecutter.github_actions_ci }}" == "No":
    sys.stderr.write("Automatic PyPI releases are currently only supported in combination with Github Actions CI")
    sys.exit(1)

if "{{ cookiecutter.codecovio }}" == "Yes" and "{{ cookiecutter.license }}" == "None":
    sys.stderr.write("Coverage reports for codecov.io require an open source license for your project")
    sys.exit(1)
