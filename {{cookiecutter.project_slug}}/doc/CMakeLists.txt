{% if cookiecutter.doxygen or cookiecutter.readthedocs %}
find_package(Doxygen REQUIRED)
set(DOXYGEN_EXCLUDE_PATTERNS "${CMAKE_SOURCE_DIR}/ext/*")
set(DOXYGEN_SHORT_NAMES YES)
{% if cookiecutter.readthedocs %}
set(DOXYGEN_GENERATE_XML YES)
{% endif %}

doxygen_add_docs({{ cookiecutter.project_slug }}-doxygen
  ${CMAKE_SOURCE_DIR}/include
{% if not cookiecutter.header_only %}
  ${CMAKE_SOURCE_DIR}/src
{% endif %}
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT Building doxygen documentation...
)
{% if cookiecutter.readthedocs %}

add_custom_target({{ cookiecutter.project_slug }}-sphinx-doc
  COMMAND
    sphinx-build -b html
    -Dbreathe_projects.{{ cookiecutter.project_slug }}="${CMAKE_CURRENT_BINARY_DIR}/xml"
    -c ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}/sphinx
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT "Generating documentation with Sphinx..."
)
add_dependencies({{ cookiecutter.project_slug }}-sphinx-doc {{ cookiecutter.project_slug }}-doxygen)
{% endif %}
{% endif %}
