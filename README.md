# Welcome to C++ Project Cookiecutter!

This repository is a template repository (a cookiecutter) that allows you to quickly
set up new CMake-based C++ projects. If you are new to C++ and CMake, you might want
to checkout out our simpler [C++ template repository](https://github.com/ssciwr/cpp-project-template).

#

# Prerequisites

In order to use this C++ Project Cookiecutter you need the following software installed:

* [Cookiecutter](https://github.com/cookiecutter/cookiecutter) e.g. by doing `pip install cookiecutter`.
* `git >= 1.8.2`

# Using C++ Project Cookiecutter

Simply run the cookiecutter command line interface:

```
cookiecutter gh:ssciwr/cookiecutter-cpp-project
```

This will start an interactive prompt that will configure and generate your project.

# Configuration

This cookiecutter accepts the following configuration options:

* `project_name`: The human-readable name of the project, defaults to `My C++ Project`
* `project_slug`: This will be the name of the generated directorym, defaults to `my-cpp-project`
* `full_name`: Author name, defaults to `Your Name`
* `license` adds a license file to the repository. It can be chosen from this list:
    * `MIT` (default)
    * `BSD-2`
    * `GPL-3.0`
    * `LGPL-3.0`
    * `None`
* `github_actions_ci`: Whether to add a CI workflow for Github Actions
* `gitlab_ci`: Whether to add a CI workflow for GitLab CI
* `travis_ci`: Whether to add a CI workflow for Travis CI
* `doxygen`: Whether a Doxygen documentation should be extracted from the project
* `cxx_minimum_standard`: The minimum C++ standard required for this project. It can be chosen from `11` (default), `14`, `17`, `20` and `03`.
* `python_bindings`: Whether to automatically add a PyBind11-based Python binding package.
* `pypi_release`: Whether to add an automatic PyPI deploy workflow to the CI system.
  This is currently limited to Github Actions CI as it provides cloud-based runners all relevant
  platforms (Linux, MacOS, Windows). A PyPI release is automatically triggered when a release is
  generated in the Github UI.

# Issues

Please report any issues you might have with template using [the Github issue
tracker](https://githab.com/ssciwr/cookiecutter-cpp-project)
