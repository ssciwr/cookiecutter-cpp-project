add_executable(tests tests.cpp {{ cookiecutter.project_slug }}_t.cpp)
target_link_libraries(tests PUBLIC {{ cookiecutter.project_slug }} Catch2::Catch2)

# allow user to run tests with `make test` or `ctest`
catch_discover_tests(tests)
