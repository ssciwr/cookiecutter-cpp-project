# Declare an executable target
add_executable({{ cookiecutter.project_slug }}_app)

# Add source files to the executable target
target_sources({{ cookiecutter.project_slug }}_app
  PRIVATE
    {{ cookiecutter.project_slug }}_app.cpp
)

# Link the executable against the library
target_link_libraries({{ cookiecutter.project_slug }}_app
  PRIVATE
    {{ cookiecutter.project_slug }}
)
