add_executable({{ cookiecutter.project_slug }}_app {{ cookiecutter.project_slug }}_app.cpp)
target_link_libraries({{ cookiecutter.project_slug }}_app PRIVATE {{ cookiecutter.project_slug }})
