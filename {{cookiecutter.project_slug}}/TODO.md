This TODO list is automatically generated from the cookiecutter-cpp-project template.
The following tasks need to be done to get a fully working project:

{% if cookiecutter.remote_url == 'None' -%}
* Set up a remote repository. You can e.g. create a project in GitHub or GitLab and run
  the following commands in your locally generated project folder: `git remote add origin <Remote-URL>`
  For a seamless integration, the name of the project should also be `{{ cookiecutter.project_slug }}`.
{%- else %}
* Push to your remote repository for the first time by doing `git push origin main`.
{%- endif %}
* Make sure that the following software is installed on your computer:
  * A C++-{{ cookiecutter.cxx_minimum_standard}}-compliant C++ compiler
  * CMake `>= 3.9`
{%- if cookiecutter.use_submodules == "No" %}
  * The testing framework [Catch2](https://github.com/catchorg/Catch2)
{%- if cookiecutter.python_bindings == "Yes" -%}
  * The [PyBind11](https://github.com/pybind/pybind11) library
{%- endif %}
{%- endif %}
{%- if cookiecutter.external_dependency != "None" %}
  * Adapt your list of external dependencies in `CMakeLists.txt` and `{{ cookiecutter.project_slug }}Config.cmake.in`.
    You can e.g.
    * Link your library or applications to your dependency. For this to work, you need
      to see if your dependency exports targets and what their name is. As this is highly
      individual, this cookiecutter could not do this for you.
    * Add more dependencies in analogy to `{{ cookiecutter.external_dependency }}`
    * Make dependencies requirements by adding `REQUIRED` to `find_package()`
    * Add version constraints to dependencies by adding `VERSION` to `find_package()`
    * Make a dependency a pure build time dependency by removing it from `{{ cookiecutter.project_slug }}Config.cmake.in`
{%- endif %}
{%- if cookiecutter.gitlab_ci == "Yes" %}
* Make sure that CI/CD pipelines are enabled in your Gitlab project settings and that
  there is a suitable Runner available. If you are using the cloud-hosted gitlab.com,
  this should already be taken care of.
{%- endif %}
{%- if cookiecutter.readthedocs == "Yes" %}
* Enable the integration of Readthedocs with your Git hoster. In the case of Github, this means
  that you need to login at [Read the Docs](https://readthedocs.org) and click the button
  *Import a Project*.
{%- endif %}
{%- if cookiecutter.doxygen == "Yes" %}
* Make sure that doxygen is installed on your system, e.g. by doing `sudo apt install doxygen`
  on Debian or Ubuntu.
{%- endif %}
{%- if cookiecutter.python_bindings == "Yes" %}
* Edit the parameters of `setup()` in `setup.py` file to contain the necessary information
  about your project, such as your email adress, PyPI classifiers and a short project description.
{%- endif %}
{%- if cookiecutter.pypi_release == "Yes" %}
* Head to your user settings at `https://pypi.org` and `https://test.pypi.org/` to setup PyPI trusted publishing.
  In order to do so, you have to head to the "Publishing" tab, scroll to the bottom
  and add a "new pending publisher". The relevant information is:
  * PyPI project name: `{{ cookiecutter|modname }}`
  * Owner: `{{ cookiecutter|username }}`
  * Repository name: `{{ cookiecutter|remote_slug }}`
  * Workflow name: `pypi.yml`
  * Environment name: not required
{%- endif %}
{%- if cookiecutter.codecovio == "Yes" %}
* Enable the integration with `codecov.io` by heading to the [Codecov.io Website](https://codecov.io),
  log in (e.g. with your Github credentials) and enable integration for your repository. In order to do
  so, you need to select it from the list of repositories (potentially re-syncing with GitHub). Then, head
  to the "Settings" Tab and select "Global Upload Token". Here, you should select the "not required" option.
{%- endif %}
