# Welcome to C++ Project Cookiecutter!

This repository is a template repository (a cookiecutter) that allows you to quickly
set up new CMake-based C++ projects. If you are new to C++ and CMake, you might want
to checkout out our simpler [C++ template repository](https://github.com/ssciwr/cpp-project-template).

# Prerequisites

In order to use this C++ Project Cookiecutter you need the following software installed:

* Python `>= 3.6`
* [Cookiecutter](https://github.com/cookiecutter/cookiecutter) e.g. by doing `pip install cookiecutter`.
* Git `>= 1.8.2`

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
* `license` adds a license file to the repository. It can be chosen from [MIT](https://opensource.org/licenses/MIT) (default), [BSD-2](https://opensource.org/licenses/BSD-2-Clause), [GPL-3.0](https://opensource.org/licenses/GPL-3.0), [LGPL-3.0](https://opensource.org/licenses/LGPL-3.0) or it can be omitted.
* `github_actions_ci`: Whether to add a CI workflow for Github Actions
* `gitlab_ci`: Whether to add a CI workflow for GitLab CI
* `travis_ci`: Whether to add a CI workflow for Travis CI
* `doxygen`: Whether a Doxygen documentation should be extracted from the project
* `cxx_minimum_standard`: The minimum C++ standard required for this project. It can be chosen from `11` (default), `14`, `17` and `20`.
  `C++03` and earlier are not supported, because the generated project will depend on libraries that require `C++11` ([Catch2](https://github.com/catchorg/Catch2)
  for testing and [pybind11](https://github.com/pybind/pybind11) for potential Python bindings).
* `python_bindings`: Whether to automatically add a PyBind11-based Python binding package.
* `pypi_release`: Whether to add an automatic PyPI deploy workflow to the CI system.
  This is currently limited to Github Actions CI as it provides cloud-based runners all relevant
  platforms (Linux, MacOS, Windows). A PyPI release is automatically triggered when a release is
  generated in the Github UI.

If you are using `cookiecutter-cpp-project` a lot, you can customize your default values
by providing a `.cookiecutterrc` file in your home directory, for more details see the
[cookiecutter documentation](https://cookiecutter.readthedocs.io/en/latest/advanced/user_config.html).

# Issues

Please report any issues you might have with template using [the Github issue
tracker](https://githab.com/ssciwr/cookiecutter-cpp-project)
