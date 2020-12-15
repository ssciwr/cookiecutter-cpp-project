cmake_minimum_required(VERSION 3.9)

# Set a name and a version number for your project:
project({{ cookiecutter.project_slug }} VERSION 0.0.1 LANGUAGES CXX)

# Define the minimum C++ standard that is required
set(CMAKE_CXX_STANDARD {{ cookiecutter.cxx_minimum_standard }})
set(CMAKE_CXX_STANDARD_REQUIRED ON)

{% if cookiecutter.python_bindings == "Yes" -%}
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
{%- endif %}
# compile the library
add_subdirectory(src)

# compile the application
add_subdirectory(app)

# compile the tests
{% if cookiecutter.use_submodules == "Yes" -%}
add_subdirectory(ext/Catch2)
include(./ext/Catch2/contrib/Catch.cmake)
{% else %}
find_package(Catch2 REQUIRED)
include(Catch)
{%- endif %}
# this needs to be in the top level CMakeLists.txt:
include(CTest)
add_subdirectory(tests)

{% if cookiecutter.doxygen == "Yes" -%}
# Add the documentation
add_subdirectory(doc)
{%- endif %}
{% if cookiecutter.python_bindings == "Yes" -%}
# Add Python bindings
{% if cookiecutter.use_submodules == "Yes" -%}
add_subdirectory(ext/pybind11)
{% else %}
find_package(pybind11)
{%- endif %}
add_subdirectory(python)
{%- endif %}

# This prints a summary of found dependencies
include(FeatureSummary)
feature_summary(WHAT ALL)
