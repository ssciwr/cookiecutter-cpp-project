# Welcome to {{ cookiecutter.project_name }}

{# The white-space control of the below template is quite delicate - if you add one, do it exactly like this (mind the -'s) -#}
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
{% if cookiecutter.github_actions_ci == "Yes" -%}
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/{{ cookiecutter.remote_url.split("/")[-2].split(":")[-1] }}/{{ cookiecutter.remote_url.replace(".git", "").split("/")[-1]}}/CI)
{% endif -%}
{% if cookiecutter.gitlab_ci == "Yes" -%}
![Gitlab pipeline status](https://img.shields.io/gitlab/pipeline/{{ cookiecutter.remote_url.split("/")[-2].split(":")[-1] }}/{{ cookiecutter.remote_url.replace(".git", "").split("/")[-1]}}/main
{%- if "gitlab.com" not in cookiecutter.gitlab_ci -%}
?gitlab_url=https%3A%2F%2F{{ cookiecutter.remote_url.replace("https://", "").replace("ssh://git@", "").split("/")[0].split(":")[0] }}
{%- endif -%}
)
{% endif -%}
{% if cookiecutter.travis_ci == "Yes" -%}
![Travis CI](https://img.shields.io/travis/com/{{ cookiecutter.remote_url.split("/")[-2].split(":")[-1] }}/{{ cookiecutter.remote_url.replace(".git", "").split("/")[-1]}})
{% endif -%}
{% endif -%}
{% if cookiecutter.pypi_release != "No" -%}
[![PyPI Release](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug.replace("-", "") }}.svg)](https://pypi.org/project/{{ cookiecutter.project_slug.replace("-", "") }})
{% endif -%}
{% if cookiecutter.readthedocs == "Yes" -%}
[![Documentation Status](https://readthedocs.org/projects/{{ cookiecutter.project_slug }}/badge/)](https://{{ cookiecutter.project_slug }}.readthedocs.io/)
{% endif -%}
{{ "\n" -}}
# Prerequisites

Building {{ cookiecutter.project_name }} requires the following software installed:

* A C++{{ cookiecutter.cxx_minimum_standard }}-compliant compiler
* CMake `>= 3.9`
{% if cookiecutter.doxygen == "Yes" or cookiecutter.readthedocs == "Yes" -%}* Doxygen (optional, documentation building is skipped if missing){% endif %}
{% if cookiecutter.python_bindings == "Yes" -%}* Python `>= 3.6` for building Python bindings{% endif %}

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
