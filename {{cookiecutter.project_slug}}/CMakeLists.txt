cmake_minimum_required(VERSION 3.9)

# Set a name and a version number for your project:
project({{ cookiecutter.project_slug }} VERSION 0.0.1 LANGUAGES CXX)

{%- if cookiecutter.external_dependency != "None" %}

# Set CMake policies for this project

# We allow <Package>_ROOT (env) variables for locating dependencies
cmake_policy(SET CMP0074 NEW)
{%- endif %}

# Initialize some default paths
include(GNUInstallDirs)

# Define the minimum C++ standard that is required
set(CMAKE_CXX_STANDARD {{ cookiecutter.cxx_minimum_standard }})
set(CMAKE_CXX_STANDARD_REQUIRED ON)

{% if cookiecutter.python_bindings == "Yes" -%}
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
{%- endif %}

# Compilation options
{%- if cookiecutter.python_bindings == "Yes" %}
option(BUILD_PYTHON "Enable building of Python bindings" OFF)
{%- endif %}
{%- if cookiecutter.doxygen == "Yes" or cookiecutter.readthedocs == "Yes" %}
option(BUILD_DOCS "Enable building of documentation" ON)
{%- endif %}

{%- if cookiecutter.external_dependency != "None" %}

# Find external dependencies
find_package({{ cookiecutter.external_dependency }})
{%- endif %}

{%- if cookiecutter.header_only == "No" %}

# compile the library
add_subdirectory(src)
{% else %}

# Add an interface target for our header-only library
add_library({{ cookiecutter.project_slug }} INTERFACE)
target_include_directories({{ cookiecutter.project_slug }} INTERFACE
  $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include/>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
{%- endif %}

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
  find_package(pybind11 REQUIRED)
  # Compile the Pybind11 module
  pybind11_add_module(_{{ cookiecutter|modname }} python/{{ cookiecutter|modname }}/_{{ cookiecutter.project_slug }}.cpp)
  target_link_libraries(_{{ cookiecutter|modname }} PUBLIC {{ cookiecutter.project_slug }})

  # Install the Python module shared library
  install(TARGETS _{{ cookiecutter|modname }} DESTINATION .)
endif()
{%- endif %}

# Add an alias target for use if this project is included as a subproject in another project
add_library({{ cookiecutter.project_slug }}::{{ cookiecutter.project_slug }} ALIAS {{ cookiecutter.project_slug }})

# Install targets and configuration
{%- if cookiecutter.external_dependency == "None" %}
install(
  TARGETS {{ cookiecutter.project_slug }}
  EXPORT {{ cookiecutter.project_slug }}-config
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(
  EXPORT {{ cookiecutter.project_slug }}-config
  NAMESPACE {{ cookiecutter.project_slug }}::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)
{%- else %}
install(
  TARGETS {{ cookiecutter.project_slug }}
  EXPORT {{ cookiecutter.project_slug }}-targets
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(
  EXPORT {{ cookiecutter.project_slug }}-targets
  FILE {{ cookiecutter.project_slug }}Targets.cmake
  NAMESPACE {{ cookiecutter.project_slug }}::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }})

include(CMakePackageConfigHelpers)
configure_package_config_file(
  ${CMAKE_CURRENT_LIST_DIR}/{{ cookiecutter.project_slug }}Config.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}Config.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }})

install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}Config.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }})

export(
  EXPORT {{ cookiecutter.project_slug }}-targets
  FILE ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}Targets.cmake
  NAMESPACE {{ cookiecutter.project_slug }}::)
{%- endif %}

install(
  DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/include/
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# This prints a summary of found dependencies
include(FeatureSummary)
feature_summary(WHAT ALL)
