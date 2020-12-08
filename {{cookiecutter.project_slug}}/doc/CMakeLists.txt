{%- if cookiecutter.doxygen == "Yes" -%}
find_package(Doxygen)
if(DOXYGEN_FOUND)
  set(DOXYGEN_EXCLUDE_PATTERNS "${CMAKE_SOURCE_DIR}/ext/*")
  set(DOXYGEN_SHORT_NAMES YES)
  doxygen_add_docs(doxygen
    ${CMAKE_SOURCE_DIR}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT Building doxygen documentation...
  )
endif()
{%- endif -%}