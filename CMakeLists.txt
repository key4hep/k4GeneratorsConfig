cmake_minimum_required(VERSION 3.25)

project(k4GeneratorsConfig LANGUAGES CXX)

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

# - Use GNU-style hierarchy for installing build products
include(GNUInstallDirs)

#--- Define basic build settings -----------------------------------------------
include(cmake/Key4hepConfig.cmake)

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
set_target_properties(eventGenerationSummary PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/$<0:>)
set_target_properties(pythiaRunner PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/$<0:>)
set_target_properties(pythiaLHERunner PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/$<0:>)
set_target_properties(key4HEPAnalysis PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/$<0:>)

configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/k4GeneratorsConfig/convertHepMC2EDM4HEP_env.sh.in
        ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/convertHepMC2EDM4HEP_env.sh @ONLY)

install(DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/ DESTINATION ${CMAKE_INSTALL_BINDIR}  FILES_MATCHING PATTERN "*env.sh*" )

install(DIRECTORY ${PROJECT_SOURCE_DIR}/python
  DESTINATION ${CMAKE_INSTALL_PREFIX}
  REGEX test_.*\\.py|main.py$ EXCLUDE  # Don't install python unittests
  PATTERN __pycache__ EXCLUDE  # Or pythons caches
)
# Install main as an executable
install(PROGRAMS ${PROJECT_SOURCE_DIR}/python/main.py DESTINATION ${CMAKE_INSTALL_PREFIX}/python)

install(CODE "execute_process(COMMAND bash -c \"set -e
    link_target=${CMAKE_INSTALL_PREFIX}/python/main.py
    link_name=${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/k4GeneratorsConfig
    rm -f $link_name
    ln -s $link_target $link_name
    \")")

# Install the share directory to make them easily accessible
install(DIRECTORY ${PROJECT_SOURCE_DIR}/share/ECFAHiggsFactories DESTINATION ${CMAKE_INSTALL_DATADIR}/${CMAKE_PROJECT_NAME})
