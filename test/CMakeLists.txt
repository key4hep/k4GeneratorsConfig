set(TEST_COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/cmake-check.sh")
set(TEST_TIMEOUT 3500)
set(TEST_ENVIRONMENT "K4GENERATORSCONFIG=${PROJECT_BINARY_DIR}/bin")

set(generatorList Babayaga KKMC Madgraph Pythia Sherpa Whizard )
foreach(generator ${generatorList})
  list(APPEND InputAndRunList InputAndRun_${generator} )
  message("Appended to list " InputAndRun_${generator} )
  message("Appended to list " ${InputAndRunList} )
endforeach()

foreach(generator ${InputAndRunList})
  message("Listing the List " ${generator})
endforeach()

add_test(NAME setupGeneratorRuns COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/cmake-check-yaml.sh" )
set_tests_properties("setupGeneratorRuns"
    PROPERTIES
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      ENVIRONMENT ${TEST_ENVIRONMENT}
)

add_test(NAME xsectionRuns COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/cmake-check-xsection.sh" )
set_tests_properties("xsectionRuns"
    PROPERTIES
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      ENVIRONMENT ${TEST_ENVIRONMENT}
      DEPENDS ${InputAndRunList}
)

function(add_custom_test name generator)
  add_test(NAME ${name}_${generator} COMMAND ${TEST_COMMAND} ${generator} -r)
  set_tests_properties(${name}_${generator}
    PROPERTIES
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      ENVIRONMENT ${TEST_ENVIRONMENT}
      TIMEOUT ${TEST_TIMEOUT}
      DEPENDS "setupGeneratorRuns"
  )
endfunction()

# Add tests using the function with simplified names
add_custom_test(InputAndRun Sherpa)
add_custom_test(InputAndRun KKMC)
add_custom_test(InputAndRun Whizard)
add_custom_test(InputAndRun Babayaga)
add_custom_test(InputAndRun Pythia)
add_custom_test(InputAndRun Madgraph)

#add_test(NAME Finalize COMMAND ${CMAKE_BINARY_DIR}/bin/xsectionSummary -f ${CMAKE_SOURCE_DIR}/test/xsectionSummary.dat)
