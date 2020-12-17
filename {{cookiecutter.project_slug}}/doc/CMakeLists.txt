{%- if cookiecutter.doxygen == "Yes" or cookiecutter.readthedocs == "Yes" -%}
find_package(Doxygen REQUIRED)
set(DOXYGEN_EXCLUDE_PATTERNS "${CMAKE_SOURCE_DIR}/ext/*")
set(DOXYGEN_SHORT_NAMES YES)
{% if cookiecutter.readthedocs == "Yes" -%}
set(DOXYGEN_GENERATE_XML YES)
{%- endif %}
doxygen_add_docs(doxygen
  ${CMAKE_SOURCE_DIR}
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT Building doxygen documentation...
)
{% if cookiecutter.readthedocs == "Yes" -%}
add_custom_target(sphinx-doc
                  COMMAND
                  sphinx-build -b html
                  -Dbreathe_projects.{{ cookiecutter.project_slug }}="${CMAKE_CURRENT_BINARY_DIR}/xml"
                  -c ${CMAKE_CURRENT_SOURCE_DIR}
                  ${CMAKE_CURRENT_SOURCE_DIR}
                  ${CMAKE_CURRENT_BINARY_DIR}/sphinx
                  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
                  COMMENT "Generating documentation with Sphinx..."
                  )
add_dependencies(sphinx-doc doxygen)
{%- endif %}
{%- endif -%}