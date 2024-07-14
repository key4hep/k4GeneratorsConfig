set(basic_sources
  ${CMAKE_CURRENT_SOURCE_DIR}/src/convertHepMC2EDM4HEP.cxx
  ${CMAKE_CURRENT_SOURCE_DIR}/src/cmdline.c
  ${CMAKE_CURRENT_SOURCE_DIR}/src/WriterEDM4HEP.cxx
)

add_executable(convertHepMC2EDM4HEP ${basic_sources})
target_include_directories(convertHepMC2EDM4HEP PRIVATE ${HEPPDT_INCLUDE_DIR})
target_link_libraries(convertHepMC2EDM4HEP PRIVATE
  EDM4HEP::edm4hep podio::podioRootIO HepMC3::HepMC3 ${HEPPDT_LIBRARIES}
)
target_compile_definitions(convertHepMC2EDM4HEP PRIVATE
  HEPMCCONVERT_EXTENSION_HEPEVTZEUS=1
  HEPMCCONVERT_EXTENSION_DOT=1
)

# Add the optional compile definitions and libraries depending on which optional
# dependencies have been found
if(ZLIB_FOUND)
  message(STATUS "HepMC3 ConvertExample: zlib found. zlib compressed files support enabled.")
  target_link_libraries(convertHepMC2EDM4HEP PRIVATE ZLIB::ZLIB)
  target_compile_definitions(convertHepMC2EDM4HEP PRIVATE
    HEPMC3_USE_COMPRESSION HEPMC3_Z_SUPPORT=1
  )
  # create environment scripts
  # #set(basic_libdir "${basic_libdir}:${ZLIB_ROOT}")
else()
  message(STATUS "HepMC3 ConvertExample: zlib not found. zlib compressed files support disabled.")
endif()

if(LIBLZMA_FOUND)
  message(STATUS "HepMC3 ConvertExample: lzma found. lzma compressed files support enabled.")
  target_link_libraries(convertHepMC2EDM4HEP PRIVATE LibLZMA::LibLZMA)
  target_compile_definitions(convertHepMC2EDM4HEP PRIVATE
    HEPMC3_USE_COMPRESSION HEPMC3_LZMA_SUPPORT=1
  )
else()
  message(STATUS "HepMC3 ConvertExample: lzma not found. lzma compressed files support disabled.")
endif()

if(BZIP2_FOUND)
  message(STATUS "HepMC3 ConvertExample: bzip2 found. bzip2 compressed files support enabled.")
  target_link_libraries(convertHepMC2EDM4HEP PRIVATE BZip2::BZip2)
  target_compile_definitions(convertHepMC2EDM4HEP PRIVATE
    HEPMC3_USE_COMPRESSION HEPMC3_BZ2_SUPPORT=1
  )
else()
  message(STATUS "HepMC3 ConvertExample: bzip not found. bzip2 compressed files support disabled.")
endif()

install(TARGETS convertHepMC2EDM4HEP
  EXPORT k4GeneratorsConfigTargets
  DESTINATION "${CMAKE_INSTALL_BINDIR}"
)

set(xsection_sources
  ${CMAKE_CURRENT_SOURCE_DIR}/src/xsectionSummary.cxx
  ${CMAKE_CURRENT_SOURCE_DIR}/src/xsection.cxx
  ${CMAKE_CURRENT_SOURCE_DIR}/src/xsectionCollection.cxx
  ${CMAKE_CURRENT_SOURCE_DIR}/src/xsection2Root.cxx
)

add_executable(xsectionSummary ${xsection_sources})
target_link_libraries(xsectionSummary PRIVATE
  EDM4HEP::edm4hep podio::podioRootIO ROOT::Tree ROOT::Hist ROOT::Gpad
)

install(TARGETS xsectionSummary
  EXPORT k4GeneratorsConfigTargets
  DESTINATION "${CMAKE_INSTALL_BINDIR}"
)

set(pythia_sources
  ${CMAKE_CURRENT_SOURCE_DIR}/src/pythiaRunner.cxx
  ${CMAKE_CURRENT_SOURCE_DIR}/src/pythiaUserHooks.cxx
)

add_executable(pythiaRunner ${pythia_sources})
target_include_directories(pythiaRunner PRIVATE ${PYTHIA8_INCLUDE_DIR} ${HEPMC3_INCLUDE_DIR})
target_link_libraries(pythiaRunner PRIVATE ${PYTHIA8_LIBRARY} HepMC3::HepMC3 )

install(TARGETS pythiaRunner
  EXPORT k4GeneratorsConfigTargets
  DESTINATION "${CMAKE_INSTALL_BINDIR}"
)
set(analyze2f_sources
  ${CMAKE_CURRENT_SOURCE_DIR}/src/analyze2f.cxx
)

add_executable(analyze2f ${analyze2f_sources})
target_link_libraries(analyze2f PRIVATE
  EDM4HEP::edm4hep podio::podioRootIO ROOT::Hist
)

install(TARGETS analyze2f
  EXPORT k4GeneratorsConfigTargets
  DESTINATION "${CMAKE_INSTALL_BINDIR}"
)

