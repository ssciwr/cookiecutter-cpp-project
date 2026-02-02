# Declare a new library target
add_library({{ cookiecutter.project_slug }})

# Add the implementation file and mark the public headers that belong to this library
target_sources({{ cookiecutter.project_slug }}
  PRIVATE
    {{ cookiecutter.project_slug }}.cpp

  PUBLIC
    FILE_SET HEADERS
    BASE_DIRS ../include
    FILES
      ../include/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}.hpp
)

# Request a minimum C++ standard for this target
target_compile_features({{ cookiecutter.project_slug }}
  PUBLIC
    cxx_std_{{ cookiecutter.cxx_minimum_standard }}
)
