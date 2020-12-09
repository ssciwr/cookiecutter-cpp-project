# Welcome to {{ cookiecutter.project_name }}

{% if cookiecutter.license == "MIT" %}[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT){% endif %}
{% if cookiecutter.license == "BSD-2" %}[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause){% endif %}
{% if cookiecutter.license == "GPL-3.0" %}[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0){% endif %}
{% if cookiecutter.license == "LGPL-3.0" %}[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0){% endif %}
{% if cookiecutter.pypi_release != "No" %}[![PyPI version](https://badge.fury.io/py/{{ cookiecutter.project_slug.replace("-", "") }}.svg)](https://badge.fury.io/py/{{ cookiecutter.project_slug.replace("-", "") }}){% endif %}

# Prerequisites

Building {{ cookiecutter.project_name }} requires the following software installed:

* A C++{{ cookiecutter.cxx_min_standard }}-compliant compiler
* CMake `>= 3.9`
{% if cookiecutter.doxygen -%}* Doxygen (optional, documentation building is skipped if missing){% endif %}
{% if cookiecutter.python_bindings -%}* Python `>= 3.6` for building Python bindings{% endif %}

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
{% if cookiecutter.doxygen %}
# Documentation

{{ cookiecutter.project_name }} provides a Doxygen documentation. You can build
the documentation locally by making sure that `Doxygen` is installed on your system
and running this command from the top-level build directory:

```
cmake -- build . --target doxygen
```

The web documentation can then be browsed by opening `doc/html/index.html` in your browser.
{% endif %}