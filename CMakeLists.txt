cmake_minimum_required(VERSION 3.27)
project(ConvertHepMC2EDM4HEP)
set(basic_sources   ${CMAKE_CURRENT_SOURCE_DIR}/k4generators/src/convertHepMC2EDM4HEP.cxx
                    ${CMAKE_CURRENT_SOURCE_DIR}/k4generators/src/cmdline.c 
		    ${CMAKE_CURRENT_SOURCE_DIR}/k4generators/src/WriterEDM4HEP.cxx )
set(basic_includes ${CMAKE_CURRENT_SOURCE_DIR}/k4generators/include ${CMAKE_CURRENT_SOURCE_DIR})
set(basic_defines HEPMCCONVERT_EXTENSION_HEPEVTZEUS=1 HEPMCCONVERT_EXTENSION_DOT=1)
set(basic_dependencies )
set(basic_libdir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}" )
add_executable(convertHepMC2EDM4HEP ${basic_sources})
find_package(HepMC3)
if(HepMC3_FOUND)
  message(STATUS "k4generators: HepMC3 found. HepMC3 support enabled. ${HEPMC3_INCLUDE_DIR} ${HEPMC3_LIBRARIES} ")
  target_link_libraries(convertHepMC2EDM4HEP PUBLIC HepMC3::HepMC3)
elseif()
  message(STATUS "k4generators: HepMC3 not found. this sucks really.")
endif()
find_package(EDM4HEP REQUIRED)
if(EDM4HEP_FOUND)
  message(STATUS "k4generators: EDM4HEP found. EDM4HEP support enabled.")
  target_link_libraries(convertHepMC2EDM4HEP PUBLIC EDM4HEP::edm4hep)
endif()
find_package(podio REQUIRED)
if(podio_FOUND)
  message(STATUS "k4generators: podio found. podio support enabled.")
  target_link_libraries(convertHepMC2EDM4HEP PUBLIC podio::podioRootIO)
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
find_package(HepPDT REQUIRED)
if(HepPDT_FOUND )
  target_include_directories(convertHepMC2EDM4HEP PUBLIC ${HEPPDT_INCLUDE_DIR} )
  target_link_libraries(convertHepMC2EDM4HEP PUBLIC ${HEPPDT_LIBRARIES})
endif()

find_package(ZLIB)
if(ZLIB_FOUND)
  message(STATUS "HepMC3 ConvertExample: zlib found. zlib compressed files support enabled. ${ZLIB_INCLUDE_DIR} ${ZLIB_LIBRARIES} ")
  list(APPEND basic_includes ${ZLIB_INCLUDE_DIR})
  list(APPEND basic_libraries ${ZLIB_LIBRARIES})
  list(APPEND basic_defines HEPMC3_USE_COMPRESSION)
  list(APPEND basic_defines HEPMC3_Z_SUPPORT=1)
  # create environment scripts
  #set(basic_libdir "${basic_libdir}:${ZLIB_ROOT}")
elseif()
  message(STATUS "HepMC3 ConvertExample: zlib not found. zlib compressed files support disabled.")
endif()
find_package(LibLZMA)
if(LIBLZMA_FOUND)
  message(STATUS "HepMC3 ConvertExample: lzma found. lzma compressed files support enabled. ${LIBLZMA_INCLUDE_DIRS} ${LIBLZMA_LIBRARIES} ")
  list(APPEND basic_includes ${LIBLZMA_INCLUDE_DIRS})
  list(APPEND basic_libraries ${LIBLZMA_LIBRARIES})
  list(APPEND basic_defines HEPMC3_USE_COMPRESSION)
  list(APPEND basic_defines HEPMC3_LZMA_SUPPORT=1)
elseif()
  message(STATUS "HepMC3 ConvertExample: lzma not found. lzma compressed files support disabled.")
endif()
find_package(BZip2)
if(BZIP2_FOUND)
  message(STATUS "HepMC3 ConvertExample: bzip2 found. bzip2 compressed files support enabled. ${BZIP2_INCLUDE_DIRS} ${BZIP2_LIBRARIES} ")
  list(APPEND basic_includes ${BZIP2_INCLUDE_DIRS})
  list(APPEND basic_libraries ${BZIP2_LIBRARIES})
  list(APPEND basic_defines HEPMC3_USE_COMPRESSION)
  list(APPEND basic_defines HEPMC3_BZ2_SUPPORT=1)
elseif()
  message(STATUS "HepMC3 ConvertExample: bzip not found. bzip2 compressed files support disabled.")
endif()
if(Protobuf_FOUND)
  list(APPEND basic_includes ${PROJECT_SOURCE_DIR}/protobufIO/include  ${Protobuf_INCLUDE_DIRS})
  list(APPEND basic_libraries ${Protobuf_LIBRARIES} HepMC3::protobufIO)
  # create environment scripts
  set(basic_libdir "${basic_libdir}:${Protobuf_LIBRARY_DIR}")
endif()


if (MSVC)
  set(  MSVCLINKFLAGS "/WHOLEARCHIVE:${PROJECT_BINARY_DIR}/outputs/${CMAKE_INSTALL_LIBDIR}/HepMC3-static.lib")
  if(ZLIB_FOUND)
    set(  MSVCLINKFLAGS "${MSVCLINKFLAGS} /WHOLEARCHIVE:${ZLIB_LIBRARIES}")
  endif()
  set_target_properties(convertHepMC2EDM4HEP PROPERTIES LINK_FLAGS ${MSVCLINKFLAGS})
endif()
include_directories(${basic_includes})
target_link_libraries(convertHepMC2EDM4HEP PUBLIC ${basic_libraries} )
target_compile_definitions(convertHepMC2EDM4HEP PRIVATE ${basic_defines} )
if (basic_dependencies)
  add_dependencies( convertHepMC2EDM4HEP ${basic_dependencies} )
endif()
# create environment scripts
set(bindir "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}")
set(libdir ${basic_libdir})
set_target_properties(convertHepMC2EDM4HEP PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/$<0:>)

configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/k4generators/convertHepMC2EDM4HEP_env.sh.in
        ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/convertHepMC2EDM4HEP_env.sh @ONLY)

# installs
if (USE_INSTALLED_HEPMC3)
  install(TARGETS convertHepMC2EDM4HEP DESTINATION ${CMAKE_INSTALL_BINDIR})
  install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} DESTINATION ${CMAKE_INSTALL_BINDIR} FILES_MATCHING PATTERN "*.pcm" PATTERN "*config"  PATTERN "CMakeFiles" PATTERN  "*.ilk"  EXCLUDE)
  install(DIRECTORY ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/ DESTINATION ${CMAKE_INSTALL_BINDIR}  FILES_MATCHING PATTERN "*env.sh*" )
endif()

#This is an option for developers only
if ( HEPMC3_USE_GENGETOPT )
  find_program(GENGETOPT gengetopt)
  if( NOT GENGETOPT )
    message( STATUS  "HepMC3 examples: gengetopt not found. Old scripts for options parsing will be used." )
  else()
    message( STATUS  "HepMC3 examples: gengetopt found in ${GENGETOPT}. New scripts for options parsing can be generated." )
    add_custom_command(
      OUTPUT  ${CMAKE_CURRENT_SOURCE_DIR}/cmdline.c ${CMAKE_CURRENT_SOURCE_DIR}/cmdline.h
      COMMAND ${GENGETOPT} -N --no-version --input=${CMAKE_CURRENT_SOURCE_DIR}/cmdline.ggo
      --file-name cmdline --output-dir=${CMAKE_CURRENT_SOURCE_DIR}
      --include-getopt --show-required --unnamed-opts=\"inputfile outputfile\"
      DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/cmdline.ggo
      COMMENT        "HepMC3 examples: Generating getopt parser code..."
    )
  endif()
  add_custom_target( cmdlineoptions DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/cmdline.c ${CMAKE_CURRENT_SOURCE_DIR}/cmdline.h)
  add_dependencies(  convertHepMC2EDM4HEP cmdlineoptions )
endif()


