cmake_minimum_required(VERSION 3.23)

# Set a name and a version number for your project:
project({{ cookiecutter.project_slug }}
  VERSION 0.0.1
  LANGUAGES CXX
)

# Initialize some default paths
include(GNUInstallDirs)

{% if cookiecutter.python_bindings == "Yes" -%}
# Enable PIC for Python bindings
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
{%- endif %}

{%- if cookiecutter.python_bindings == "Yes" or cookiecutter.doxygen == "Yes" or cookiecutter.readthedocs == "Yes" %}
# Compilation options
{%- endif %}
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
# Compile the library
add_subdirectory(src)
{% else %}

# Add an interface target for the header-only library
add_library({{ cookiecutter.project_slug }} INTERFACE)

# Add the public headers that belong to this library
target_sources({{ cookiecutter.project_slug }}
  INTERFACE
    FILE_SET HEADERS
    BASE_DIRS include
    FILES
      include/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}.hpp
)

# Request a minimum C++ standard for this target
target_compile_features({{ cookiecutter.project_slug }} INTERFACE cxx_std_{{ cookiecutter.cxx_minimum_standard }})
{%- endif %}

# Compile the application executable
add_subdirectory(app)

# Compile the tests
include(CTest)
if(BUILD_TESTING)
  {%- if cookiecutter.use_submodules == "Yes" %}
  add_subdirectory(ext/Catch2)
  include(./ext/Catch2/extras/Catch.cmake)
  {%- endif %}
  add_subdirectory(tests)
endif()

{% if cookiecutter.doxygen == "Yes" -%}
# Add the documentation
if(BUILD_DOCS)
  add_subdirectory(doc)
endif()
{%- endif %}

{%- if cookiecutter.python_bindings == "Yes" %}
# Add Python bindings
if(BUILD_PYTHON)
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

{%- if cookiecutter.external_dependency == "None" %}
# Install the library target and its public headers
install(
  TARGETS {{ cookiecutter.project_slug }}
  EXPORT {{ cookiecutter.project_slug }}-config
  FILE_SET HEADERS
)

# Export the installed target into a simple <Project>-config file, so that find_package({{ cookiecutter.project_slug }}) works for consumers
install(
  EXPORT {{ cookiecutter.project_slug }}-config
  NAMESPACE {{ cookiecutter.project_slug }}::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)
{%- else %}
# Install the build target and record it in an export set.
install(
  TARGETS {{ cookiecutter.project_slug }}
  EXPORT {{ cookiecutter.project_slug }}-targets
  FILE_SET HEADERS
)

# Export the target definition so other CMake projects can reconstruct the imported target via find_package()
install(
  EXPORT {{ cookiecutter.project_slug }}-targets
  FILE {{ cookiecutter.project_slug }}Targets.cmake
  NAMESPACE {{ cookiecutter.project_slug }}::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)

# Generate a <Project>Config.cmake file from a template
include(CMakePackageConfigHelpers)
configure_package_config_file(
  ${CMAKE_CURRENT_LIST_DIR}/{{ cookiecutter.project_slug }}Config.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}Config.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)

# Install the generated project configuration file alongside the targets
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}Config.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)

# Export targets for the build tree
export(
  EXPORT {{ cookiecutter.project_slug }}-targets
  FILE ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}Targets.cmake
  NAMESPACE {{ cookiecutter.project_slug }}::
)
{%- endif %}

# This prints a summary of found dependencies
include(FeatureSummary)
feature_summary(WHAT ALL)
