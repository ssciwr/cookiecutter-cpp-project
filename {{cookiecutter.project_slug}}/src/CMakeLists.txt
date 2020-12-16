add_library({{ cookiecutter.project_slug }} {{ cookiecutter.project_slug }}.cpp)
target_include_directories({{ cookiecutter.project_slug }} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include/>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

# Add an alias for use if this project is included as a subproject in another project
add_library({{ cookiecutter.project_slug }}::{{ cookiecutter.project_slug }} ALIAS {{ cookiecutter.project_slug }})
