add_library({{ cookiecutter.project_slug }} {{ cookiecutter.project_slug }}.cpp)
target_include_directories({{ cookiecutter.project_slug }} PUBLIC ../include)
target_compile_features({{ cookiecutter.project_slug }} PUBLIC cxx_std_11)
