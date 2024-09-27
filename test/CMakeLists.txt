set(TEST_COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/cmake-check.sh")
set(TEST_TIMEOUT 3500)
set(TEST_ENVIRONMENT "K4GENERATORSCONFIG=${PROJECT_BINARY_DIR}/bin")

# the generators to be run
set(generatorList Babayaga KKMC Madgraph Pythia Sherpa Whizard )

# generato the run list for the dependencies
foreach(generator ${generatorList})
  list(APPEND InputAndRunList InputAndRun_${generator})
  message(${generator} " appended to the runlist ")
endforeach()

# add the first test: setting up and comapring the yaml files
add_test(NAME setupGeneratorRuns COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/cmake-check-yaml.sh" )
set_tests_properties("setupGeneratorRuns"
    PROPERTIES
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      ENVIRONMENT ${TEST_ENVIRONMENT}
      FIXTURES_SETUP  processYamls
)

set_tests_properties(createDB   PROPERTIES )

# second test running the generators
function(add_custom_test name generator)
  add_test(NAME ${name}_${generator} COMMAND ${TEST_COMMAND} ${generator} -r)
  set_tests_properties(${name}_${generator}
    PROPERTIES
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      ENVIRONMENT ${TEST_ENVIRONMENT}
      TIMEOUT ${TEST_TIMEOUT}
      FIXTURES_REQUIRED processYamls
  )
endfunction()

# Add tests using the function with simplified names
foreach(generator ${generatorList})
  add_custom_test(InputAndRun ${generator} )
endforeach()
#add_custom_test(InputAndRun Sherpa)
#add_custom_test(InputAndRun KKMC)
#add_custom_test(InputAndRun Whizard)
#add_custom_test(InputAndRun Babayaga)
#add_custom_test(InputAndRun Pythia)
#add_custom_test(InputAndRun Madgraph)

# thirs test (after all others have been run: gather the xsections
add_test(NAME xsectionRuns COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/cmake-check-xsection.sh" )
set_tests_properties("xsectionRuns"
    PROPERTIES
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      ENVIRONMENT ${TEST_ENVIRONMENT}
      DEPENDS "${InputAndRunList}"
)

#add_test(NAME Finalize COMMAND ${CMAKE_BINARY_DIR}/bin/xsectionSummary -f ${CMAKE_SOURCE_DIR}/test/xsectionSummary.dat)
