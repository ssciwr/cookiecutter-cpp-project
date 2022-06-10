#########################################################################################
# conan_install(): Set up and manage conan dependencies via Find<X>.cmake scripts
#
# Usage:
#     conan_install(IN_DIR <directory> OUT_DIR <directory> BUILD_TYPE <Release|Debug>)
#
# Arguments (all required):
#
#     IN_DIR: Directory containing conanfile.txt or conanfile.py (likely ${CMAKE_SOURCE_DIR})
#
#     OUT_DIR: Output directory for the Find<X>.cmake scripts (this directory must be on CMAKE_MODULE_PATH)
#
#     BUILD_TYPE: "Debug" or "Release" (Likely ${CMAKE_BUILD_TYPE}, but be careful in multi-configuration
#                 tool chains like Visual Studio)
#
function(conan_install)

    # parse function arguments
    set(optionArgs)
    set(oneValueArgs IN_DIR OUT_DIR BUILD_TYPE)
    set(multiValueArgs)

    cmake_parse_arguments(CONAN_SETUP "${optionArgs}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

    # Install Conan dependencies
    message(STATUS "Looking for conanfile in ${CONAN_SETUP_IN_DIR}")

    if(EXISTS "${CONAN_SETUP_IN_DIR}/conanfile.txt" OR EXISTS "${CONAN_SETUP_IN_DIR}/conanfile.py")

        message(STATUS "Setting up conan dependencies...")

        # check that conan is installed
        find_program(CONAN_EXE conan)
        if(NOT CONAN_EXE)
            message(FATAL_ERROR "Conan not found! Conan (http://conan.io) is required to build this project.")
        endif() 

        # run conan install to create Find<X>.cmake files for dependencies
        # (will download and build the packages as needed)
        execute_process(
            COMMAND ${CONAN_EXE} install ${CONAN_SETUP_IN_DIR} -if=${CONAN_SETUP_OUT_DIR} -b=missing -sbuild_type=${CONAN_SETUP_BUILD_TYPE} -g=cmake_find_package
            WORKING_DIRECTORY ${CONAN_SETUP_IN_DIR}
            COMMAND_ERROR_IS_FATAL ANY
        )

        message(STATUS "Done setting up conan dependencies.")

    else()

        message(STATUS "No conanfile present.")

    endif()

endfunction()



