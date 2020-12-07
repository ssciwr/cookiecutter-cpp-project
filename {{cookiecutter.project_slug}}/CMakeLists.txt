cmake_minimum_required(VERSION 3.9)

# Set a name and a version number for your project:
project({{ cookiecutter.project_slug }} VERSION 0.0.1 LANGUAGES CXX)

# this needs to be in the top level CMakeLists.txt:
include(CTest)

{% if cookiecutter.python_bindings == "Yes" -%}
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
{%- endif %}

# compile the library
add_subdirectory(src)

# compile the application
add_subdirectory(app)

# compile the tests
add_subdirectory(ext/Catch2)
add_subdirectory(tests)

{% if cookiecutter.doxygen == "Yes" -%}
# Add the documentation
add_subdirectory(doc)
{%- endif %}

{% if cookiecutter.python_bindings == "Yes" -%}
# Add Python bindings
add_subdirectory(ext/pybind11)
add_subdirectory(python)
{%- endif %}
