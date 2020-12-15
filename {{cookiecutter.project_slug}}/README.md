# Welcome to {{ cookiecutter.project_name }}

{# The white-space control of the below template is quite delicate - if you add one, do it exactly like this (mind the -'s) -#}
{%- set is_github = "github.com" in cookiecutter.remote_url -%}
{%- set is_gitlab = "gitlab" in cookiecutter.remote_url -%}
{%- set username = "None" if cookiecutter.remote_url == "None" else cookiecutter.remote_url.split("/")[-2].split(":")[-1] -%}
{%- set remote_slug = "None" if cookiecutter.remote_url == "None" else cookiecutter.remote_url.replace(".git", "").split("/")[-1] -%}
{%- set gitlab_instance = "None" if cookiecutter.remote_url == "None" else "https%3A%2F%2F" + cookiecutter.remote_url.replace("https://", "").replace("ssh://git@", "").split("/")[0].split(":")[0] -%}
{%- set python_package = cookiecutter.project_slug.replace("-", "") -%}
{% if cookiecutter.license == "MIT" -%}
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
{% endif -%}
{% if cookiecutter.license == "BSD-2" -%}
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
{% endif -%}
{% if cookiecutter.license == "GPL-3.0" -%}
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
{% endif -%}
{% if cookiecutter.license == "LGPL-3.0" -%}
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
{% endif -%}
{% if cookiecutter.remote_url != "None" -%}
{% if cookiecutter.github_actions_ci == "Yes" and is_github -%}
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/{{ username }}/{{ remote_slug }}/CI)](https://github.com/{{ username }}/{{ remote_slug }}/actions?query=workflow%3ACI)
{% endif -%}
{% if cookiecutter.gitlab_ci == "Yes" and is_gitlab -%}
[![Gitlab pipeline status](https://img.shields.io/gitlab/pipeline/{{ username }}/{{ remote_slug }}/main
{%- if "gitlab.com" not in cookiecutter.remote_url -%}
?gitlab_url={{ gitlab_instance }}
{%- endif -%}
)]({{ gitlab_instance }}/{{ username }}/{{ remote_slug }}/-/pipelines)
{% endif -%}
{% endif -%}
{% if cookiecutter.pypi_release != "No" -%}
[![PyPI Release](https://img.shields.io/pypi/v/{{ python_package }}.svg)](https://pypi.org/project/{{ python_package }})
{% endif -%}
{% if cookiecutter.readthedocs == "Yes" -%}
[![Documentation Status](https://readthedocs.org/projects/{{ remote_slug }}/badge/)](https://{{ remote_slug }}.readthedocs.io/)
{% endif -%}
{{ "\n" -}}
# Prerequisites

Building {{ cookiecutter.project_name }} requires the following software installed:

* A C++{{ cookiecutter.cxx_minimum_standard }}-compliant compiler
* CMake `>= 3.9`
{% if cookiecutter.doxygen == "Yes" or cookiecutter.readthedocs == "Yes" -%}* Doxygen (optional, documentation building is skipped if missing){% endif %}
{% if cookiecutter.use_submodules == "No" -%}* The testing framework [Catch2](https://github.com/catchorg/Catch2) for building the test suite{%- endif %}
{% if cookiecutter.python_bindings == "Yes" -%}* Python `>= 3.6` for building Python bindings{% endif %}
{% if cookiecutter.use_submodules == "No" and cookiecutter.python_bindings == "Yes" -%}* The [PyBind11](https://github.com/pybind/pybind11) library for building Python bindings{%- endif %}

# Building {{ cookiecutter.project_name }}

The following sequence of commands builds {{ cookiecutter.project_name }}.
It assumes that your current working directory is the top-level directory
of the freshly cloned repository:

```
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```

# Documentation
{% if cookiecutter.readthedocs == "Yes" %}
{{ cookiecutter.project_name }} provides a Sphinx-based documentation, that can
be browsed [online at readthedocs.org](https://{{ cookiecutter.project_slug }}.readthedocs.io).
{% elif cookiecutter.doxygen == "Yes" %}
{{ cookiecutter.project_name }} provides a Doxygen documentation. You can build
the documentation locally by making sure that `Doxygen` is installed on your system
and running this command from the top-level build directory:

```
cmake --build . --target doxygen
```

The web documentation can then be browsed by opening `doc/html/index.html` in your browser.
{% else %}
{{ cookiecutter.project_name }} *should* provide a documentation.
{% endif %}
