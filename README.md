# Welcome to C++ Project Cookiecutter!

This repository is a template repository (a cookiecutter) that allows you to quickly
set up new CMake-based C++ projects. If you are new to C++ and CMake, you might want
to checkout our simpler [C++ template repository](https://github.com/ssciwr/cpp-project-template).

# Features

The core features of our C++ Cookiecutter in a nutshell:

* Very simple, configurable setup of a fully functional C++ project
* Choose and add a license and copyright statement to your project
* Ready-to-use integration with the Github Actions and Gitlab CI
* Generation and deployment of Sphinx-based documentation for [Read the Docs](https://readthedocs.org)
* Building a Doxygen documentation
* Setup of Python bindings with Pybind11
* CI-based deployment of Python bindings to PyPI
* Integration with coverage testing from [codecov.io](https://codecov.io)
* Integration with code quality analysis from [sonarcloud.io](https://sonarcloud.io/)
* Based on an established tool: [Cookiecutter](https://github.com/cookiecutter/cookiecutter) has >13k stars on Github!

# Prerequisites

In order to use this C++ Project Cookiecutter you need the following software installed:

* Python `>= 3.6`
* [Cookiecutter](https://github.com/cookiecutter/cookiecutter) e.g. by doing `pip install cookiecutter`.
* Git `>= 1.8.2`

In addition, the project that is generated from this cookiecutter will require the following software:

* A C++ compiler, e.g. `g++` or `clang++`
* CMake `>= 3.9`
* Doxygen (optional, but recommended)

# Using C++ Project Cookiecutter

Simply run the cookiecutter command line interface:

```
cookiecutter gh:ssciwr/cookiecutter-cpp-project
```

This will start an interactive prompt that will configure and generate your project.
One of the prompts will ask you for a remote repository URL, so you should head to
the Git hosting service of your choice and add a new empty repository e.g. [on Github](https://github.com/new).

# Configuration

This cookiecutter accepts the following configuration options:

* `project_name`: The human-readable name of the project, defaults to `My C++ Project`
* `remote_url`: The remote URL for the newly created repository. This is not only used
  to add it as a remote to the Git repository, but also to enable integration with some
  services. Defaults to `None` although we strongly advise you to specify it.
* `project_slug`: This will be the name of the generated directory. By default, it is deduced
  from the specified remote URL and the given project name.
* `full_name`: Author name, defaults to `Your Name`
* `license` adds a license file to the repository. It can be chosen from [MIT](https://opensource.org/licenses/MIT) (default), [BSD-2](https://opensource.org/licenses/BSD-2-Clause), [GPL-3.0](https://opensource.org/licenses/GPL-3.0), [LGPL-3.0](https://opensource.org/licenses/LGPL-3.0) or it can be omitted.
* `use_submodules`: Whether `git submodule` should be used to add version-pinned external
  dependencies (like e.g. the testing framework `Catch2`). If you do not know what git submodules
  are, you should select `No`.
* `github_actions_ci`: Whether to add a CI workflow for Github Actions
* `gitlab_ci`: Whether to add a CI workflow for GitLab CI
* `readthedocs`: Whether to create a Sphinx-documentation that can automatically be deployed to readthedocs.org
* `doxygen`: Whether a Doxygen documentation should be extracted from the project
* `cxx_minimum_standard`: The minimum C++ standard required for this project. It can be chosen from `11` (default), `14`, `17` and `20`.
  `C++03` and earlier are not supported, because the generated project will depend on libraries that require `C++11` ([Catch2](https://github.com/catchorg/Catch2)
  for testing and [pybind11](https://github.com/pybind/pybind11) for potential Python bindings).
* `python_bindings`: Whether to automatically add a PyBind11-based Python binding package.
* `pypi_release`: Whether to add an automatic PyPI deploy workflow to the CI system.
  This is currently limited to Github Actions CI as it provides cloud-based runners for all relevant
  platforms (Linux, MacOS, Windows). A PyPI release is automatically triggered when a release is
  generated in the Github UI.
* `codecovio`: Whether an automatic integration with coverage checking from [codecov.io](https://codecov.io)
  should be set up. This requires an Open Source license in order to be free to use.
* `sonarcloud`: Whether an automatic integration with code quality analysis from [sonarcloud.io](https://sonarcloud.io/)
  should be set up. Sonarcloud requires an Open Source license in order to be free to use.
  This feature requires a bit of setup, but will give you access to a very powerful code
  analysis tool. Currently, we only support SonarCloud analysis in combination with Github
  Actions CI and a Github remote repository.

If you are using `cookiecutter-cpp-project` a lot, you can customize your default values
by providing a `.cookiecutterrc` file in your home directory, for more details see the
[cookiecutter documentation](https://cookiecutter.readthedocs.io/en/latest/advanced/user_config.html).

# Issues

Please report any issues you might have with template using [the Github issue
tracker](https://github.com/ssciwr/cookiecutter-cpp-project/issues)
