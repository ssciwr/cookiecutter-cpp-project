# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
repo_root = Path(__file__).resolve().parent.parent
python_package_src = repo_root / "python" / "{{ cookiecutter.project_slug }}" / "src"

sys.path.insert(0, str(python_package_src))

# -- Project information -----------------------------------------------------

project = "{{ cookiecutter.project_slug }}"
copyright = "{{ current_year }}, {{ cookiecutter.full_name }}"
author = "{{ cookiecutter.full_name }}"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "breathe",
    "sphinx.ext.autodoc",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Breathe Configuration: Breathe is the bridge between the information extracted
# from the C++ sources by Doxygen and Sphinx.
breathe_projects = {
    "{{ cookiecutter.project_slug }}": str(repo_root / "build" / "documentation" / "doc" / "xml"),
}
breathe_default_project = "{{ cookiecutter.project_slug }}"
