cmake_minimum_required(VERSION 3.9)

# Set a name and a version number for your project:
project({{ cookiecutter.project_slug }} VERSION 0.0.1 LANGUAGES CXX)

# Define the minimum C++ standard that is required
set(CMAKE_CXX_STANDARD {{ cookiecutter.cxx_minimum_standard }})
set(CMAKE_CXX_STANDARD_REQUIRED ON)

{% if cookiecutter.python_bindings == "Yes" -%}
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
{%- endif %}

# Compilation options
{%- if cookiecutter.python_bindings == "Yes" %}
set(BUILD_PYTHON ON CACHE BOOL "Enable building of Python bindings")
{%- endif %}
{%- if cookiecutter.doxygen == "Yes" or cookiecutter.readthedocs == "Yes" %}
set(BUILD_DOCS ON CACHE BOOL "Enable building of documentation")
{%- endif %}

# compile the library
add_subdirectory(src)

# compile the application
add_subdirectory(app)

# compile the tests
include(CTest)
if(BUILD_TESTING)
  {%- if cookiecutter.use_submodules == "Yes" %}
  add_subdirectory(ext/Catch2)
  include(./ext/Catch2/contrib/Catch.cmake)
  {%- else %}
  find_package(Catch2 REQUIRED)
  include(Catch)
  {%- endif %}
  add_subdirectory(tests)
endif()

{% if cookiecutter.doxygen == "Yes" -%}
if(BUILD_DOCS)
  # Add the documentation
  add_subdirectory(doc)
endif()
{%- endif %}
{%- if cookiecutter.python_bindings == "Yes" %}
if(BUILD_PYTHON)
  # Add Python bindings
  {%- if cookiecutter.use_submodules == "Yes" %}
  add_subdirectory(ext/pybind11)
  {% else %}
  find_package(pybind11)
  {%- endif %}
  add_subdirectory(python)
endif()
{%- endif %}

# This prints a summary of found dependencies
include(FeatureSummary)
feature_summary(WHAT ALL)
