pybind11_add_module({{ cookiecutter.project_slug.replace("-", "") }}_python {{ cookiecutter.project_slug }}_python.cpp)
target_link_libraries({{ cookiecutter.project_slug.replace("-", "") }}_python PUBLIC {{ cookiecutter.project_slug}})
