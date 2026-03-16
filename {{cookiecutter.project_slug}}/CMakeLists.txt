cmake_minimum_required(VERSION 3.23)

# Set a name and a version number for your project:
project({{ cookiecutter.project_slug }}
  VERSION 0.0.1
  LANGUAGES CXX
)

# Initialize some default paths
include(GNUInstallDirs)

# Define build options
option({{ cookiecutter.project_slug }}_BUILD_TESTING "Enable building of tests" OFF)
{%- if cookiecutter.python_bindings != "None" %}

if(PROJECT_IS_TOP_LEVEL)
  option({{ cookiecutter.project_slug }}_BUILD_PYTHON "Enable building of Python bindings" ON)
else()
  option({{ cookiecutter.project_slug }}_BUILD_PYTHON "Enable building of Python bindings" OFF)
endif()
{%- endif -%}
{% if cookiecutter.doxygen == "Yes" or cookiecutter.readthedocs == "Yes" %}

if(PROJECT_IS_TOP_LEVEL)
  option({{ cookiecutter.project_slug }}_BUILD_DOCS "Enable building of documentation" ON)
else()
  option({{ cookiecutter.project_slug }}_BUILD_DOCS "Enable building of documentation" OFF)
endif()
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
target_compile_features({{ cookiecutter.project_slug }}
  INTERFACE
    cxx_std_{{ cookiecutter.cxx_minimum_standard }}
)
{%- endif %}

if(PROJECT_IS_TOP_LEVEL)
  # Compile the application executable
  add_subdirectory(app)
endif()

if(PROJECT_IS_TOP_LEVEL)
  # Compile the tests
  include(CTest)
  if({{ cookiecutter.project_slug }}_BUILD_TESTING)
  {%- if cookiecutter.use_submodules == "Yes" %}
    add_subdirectory(ext/Catch2)
  {%- endif %}
    add_subdirectory(tests)
  endif()
endif()
{%- if cookiecutter.doxygen == "Yes" %}

# Add the documentation
if(PROJECT_IS_TOP_LEVEL AND {{ cookiecutter.project_slug }}_BUILD_DOCS)
  add_subdirectory(doc)
endif()
{%- endif %}
{% if cookiecutter.python_bindings != "None" %}
# Add Python bindings
if(PROJECT_IS_TOP_LEVEL AND {{ cookiecutter.project_slug }}_BUILD_PYTHON)
  # Enable PIC for Python bindings
  set_target_properties({{ cookiecutter.project_slug }}
    PROPERTIES
      POSITION_INDEPENDENT_CODE ON
  )

  {% if cookiecutter.python_bindings == "pybind11" -%}
  set(PYBIND11_FINDPYTHON ON)
  find_package(pybind11 REQUIRED)
  # Compile the Pybind11 module
  pybind11_add_module(_{{ cookiecutter|modname }} python/{{ cookiecutter|modname }}/_{{ cookiecutter.project_slug }}.cpp)
  {% elif cookiecutter.python_bindings == "nanobind" %}
  find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

  # Detect the installed nanobind package and import it into CMake
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT
  )
  find_package(nanobind CONFIG REQUIRED)
  nanobind_add_module(_{{ cookiecutter|modname }} python/{{ cookiecutter|modname }}/_{{ cookiecutter.project_slug }}.cpp)
  {%- endif %}
  target_link_libraries(_{{ cookiecutter|modname }}
    PUBLIC
      {{ cookiecutter.project_slug }}
  )
  # Install the Python module shared library
  install(TARGETS _{{ cookiecutter|modname }} DESTINATION .)
endif()
{% endif %}
# Add an alias target for use if this project is included as a subproject in another project
add_library({{ cookiecutter.project_slug }}::{{ cookiecutter.project_slug }} ALIAS {{ cookiecutter.project_slug }})

# Install the target and headers
install(
  TARGETS {{ cookiecutter.project_slug }}
  EXPORT {{ cookiecutter.project_slug }}Targets
  FILE_SET HEADERS
)

# Install the exported targets (this creates {{ cookiecutter.project_slug }}Targets.cmake)
install(
  EXPORT {{ cookiecutter.project_slug }}Targets
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
  NAMESPACE {{ cookiecutter.project_slug }}::
)

# Include helpers for calling configure_package_config_file
include(CMakePackageConfigHelpers)

# Generate the {{ cookiecutter.project_slug }}Config.cmake file
configure_package_config_file(
  ${CMAKE_CURRENT_LIST_DIR}/cmake/{{ cookiecutter.project_slug }}Config.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}Config.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)

# Install the generated Config file
install(
  FILES
    ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}Config.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)

# Generate a version file
write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}ConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion
)

# Install the version file
install(
  FILES
    ${CMAKE_CURRENT_BINARY_DIR}/{{ cookiecutter.project_slug }}ConfigVersion.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)

# This prints a summary of found dependencies
include(FeatureSummary)
feature_summary(WHAT ALL)
