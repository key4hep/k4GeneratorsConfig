cmake_minimum_required(VERSION 3.27)

project(k4GeneratorsConfig)

# project version
SET( ${PROJECT_NAME}_VERSION_MAJOR 0 )
SET( ${PROJECT_NAME}_VERSION_MINOR 0 )
SET( ${PROJECT_NAME}_VERSION_PATCH 1 )

SET( ${PROJECT_NAME}_VERSION  "${${PROJECT_NAME}_VERSION_MAJOR}.${${PROJECT_NAME}_VERSION_MINOR}.${${PROJECT_NAME}_VERSION_PATCH}" )

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

find_package(podio REQUIRED)
find_package(EDM4HEP REQUIRED)
find_package(HepMC3 REQUIRED)
find_package(HepPDT REQUIRED)
find_package(pythia8 REQUIRED)

# --- optional dependencies for additional functionality via HepMC3
find_package(ZLIB)
find_package(LibLZMA)
find_package(BZip2)

#--- Define basic build settings -----------------------------------------------
# - Use GNU-style hierarchy for installing build products
include(GNUInstallDirs)

# - Define a default build type when using a single-mode tool like make/ninja
# If you're using a build tool that supports multiple modes (Visual Studio,
# Xcode), this setting has no effect.
# HSF recommend RelWithDebInfo (optimized with debugging symbols) as this is
# generally the mode used by system packaging (rpm, deb, spack, macports).
# However, it can be overriden by passing ``-DCMAKE_BUILD_TYPE=<type>`` when
# invoking CMake
if(NOT CMAKE_CONFIGURATION_TYPES)
  if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE RelWithDebInfo
      CACHE STRING "Choose the type of build, options are: None Release MinSizeRel Debug RelWithDebInfo"
      FORCE
      )
  else()
    set(CMAKE_BUILD_TYPE "${CMAKE_BUILD_TYPE}"
      CACHE STRING "Choose the type of build, options are: None Release MinSizeRel Debug RelWithDebInfo"
      FORCE
      )
  endif()
endif()

# - Define the C++ Standard to use (Simplest Possible)
set(CMAKE_CXX_STANDARD 17 CACHE STRING "")

if(NOT CMAKE_CXX_STANDARD MATCHES "17|20")
  message(FATAL_ERROR "Unsupported C++ standard: ${CMAKE_CXX_STANDARD}")
endif()

# Prevent CMake falls back to the latest standard the compiler does support
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Disables the use of compiler-specific extensions, hence makes sure the code
# works for a wider range of compilers
set(CMAKE_CXX_EXTENSIONS OFF)

# Build the converter
add_subdirectory(k4GeneratorsConfig)

#--- enable testing capabilities ------------------------------------------
include(CTest)

add_subdirectory(test)

# set(basic_defines)
set(basic_libdir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}" )

# create environment scripts
set(bindir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}")
set(libdir ${basic_libdir})
set_target_properties(convertHepMC2EDM4HEP PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/$<0:>)
set_target_properties(xsectionSummary PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/$<0:>)
set_target_properties(pythiaRunner PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/$<0:>)

configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/k4GeneratorsConfig/convertHepMC2EDM4HEP_env.sh.in
        ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/convertHepMC2EDM4HEP_env.sh @ONLY)

install(DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/ DESTINATION ${CMAKE_INSTALL_BINDIR}  FILES_MATCHING PATTERN "*env.sh*" )

install(DIRECTORY ${PROJECT_SOURCE_DIR}/python
  DESTINATION python
  REGEX test_.*\\.py$ EXCLUDE  # Don't install python unittests
  PATTERN __pycache__ EXCLUDE  # Or pythons caches
)
