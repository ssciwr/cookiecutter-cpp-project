{%- if cookiecutter.use_submodules == "No" %}
# Enable CMake's FetchContent module, which allows downloading dependencies like Catch2 automatically at configure time.
include(FetchContent)

# Declare a dependency on Catch2 via FetchContent. This will clone the Catch2 GitHub repository during configuration.
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v{{ cookiecutter._catch_version }})

# Make Catch2 available in this project. This defines the imported targets Catch2::Catch2 and Catch2::Catch2WithMain.
FetchContent_MakeAvailable(Catch2)

# Include Catch2's CMake helper functions (e.g. catch_discover_tests).
include(Catch)
{%- endif %}

# Create a single test binary that compiles all test files.
add_executable(tests)

# Add the implementation file
target_sources(tests PRIVATE {{ cookiecutter.project_slug }}_t.cpp)

# Link the test binary
target_link_libraries(tests PUBLIC {{ cookiecutter.project_slug }} Catch2::Catch2WithMain)

# allow user to run tests with `make test` or `ctest`
catch_discover_tests(tests)
