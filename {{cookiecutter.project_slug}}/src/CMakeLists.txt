add_library({{ cookiecutter.project_slug }} {{ cookiecutter.project_slug }}.cpp)
target_include_directories({{ cookiecutter.project_slug }} PUBLIC ../include)
