{%- set modname = cookiecutter.project_slug.replace("-", "") -%}
# Compile the Pybind11 module
pybind11_add_module(_{{ modname }} {{ modname }}/_{{ cookiecutter.project_slug }}.cpp)
target_link_libraries(_{{ modname }} PUBLIC {{ cookiecutter.project_slug }})

# Install the Python module shared library
install(TARGETS _{{ modname }} DESTINATION .)
