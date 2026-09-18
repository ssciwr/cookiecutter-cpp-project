# This script executes before cookiecutter prompts for template variables.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html

import sys
from importlib.metadata import version


# Cookiecutter 2.7 coerces command-line and configuration overrides to booleans.
parts = tuple(int(part) for part in version("cookiecutter").split(".")[:3])
if parts < (2, 7, 0):
    sys.stderr.write("This template requires cookiecutter >= 2.7\n")
    sys.exit(1)
