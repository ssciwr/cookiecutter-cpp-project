add_executable(tests tests.cpp {{ cookiecutter.project_slug }}_t.cpp)
target_link_libraries(tests PUBLIC {{ cookiecutter.project_slug }} Catch2::Catch2)
target_compile_features(tests PUBLIC cxx_std_{{ cookiecutter.cxx_minimum_standard }})

# allow user to run tests with `make test` or `ctest`
include(../ext/Catch2/contrib/Catch.cmake)
catch_discover_tests(tests)
