cmake_minimum_required(VERSION 3.9)

# Set a name and a version number for your project:
project({{ cookiecutter.project_slug }} VERSION 0.0.1 LANGUAGES CXX)

# this needs to be in the top level CMakeLists.txt:
include(CTest)

# compile the library
add_subdirectory(src)

# compile the application
add_subdirectory(app)

# compile the tests
add_subdirectory(ext/Catch2)
add_subdirectory(tests)

# Add the documentation
{% if cookiecutter.doxygen == "Yes" -%}
add_subdirectory(doc)
{%- endif %}
