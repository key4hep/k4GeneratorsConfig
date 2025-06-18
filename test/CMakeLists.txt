# generl settings:
set(TEST_ENVIRONMENT "K4GENERATORSCONFIG=${PROJECT_BINARY_DIR}/bin")
set(TEST_TIMEOUT 3500)

# we split the execution into four steps:
set(RUN_YAMLS "${CMAKE_CURRENT_SOURCE_DIR}/createGeneratorDatacardsFromYaml.sh")
set(CHECK_DATACARDS "${CMAKE_CURRENT_SOURCE_DIR}/checkGeneratorDatacards.sh")
set(RUN_GENERATORS "${CMAKE_CURRENT_SOURCE_DIR}/runEventGeneration.sh")
set(RUN_SUMMARY "${CMAKE_CURRENT_SOURCE_DIR}/runSummary.sh")

# the generators to be run
set(generatorList Babayaga KKMC Madgraph Pythia Sherpa Whizard )

# generate the run list for the dependencies
foreach(generator ${generatorList})
  list(APPEND RunList Run_${generator})
  message(${generator} " appended to the runlist ")
endforeach()

# add the whizard debug
add_test(NAME WhizardDebug COMMAND runWhizard.sh )
set_tests_properties("WhizardDebug"
  PROPERTIES
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  ENVIRONMENT ${TEST_ENVIRONMENT}
)

# add the first test: setting up and comapring the yaml files
add_test(NAME createGeneratorDatacards COMMAND ${RUN_YAMLS} )
set_tests_properties("createGeneratorDatacards"
  PROPERTIES
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  ENVIRONMENT ${TEST_ENVIRONMENT}
  FIXTURES_SETUP  "processYamls"
)

# add the first test: setting up and comapring the yaml files
function(check_generator_datacards generator)
  add_test(NAME checkGeneratorDatacards_${generator} COMMAND ${CHECK_DATACARDS} -g ${generator})
  set_tests_properties("checkGeneratorDatacards_${generator}"
    PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    ENVIRONMENT ${TEST_ENVIRONMENT}
    FIXTURES_REQUIRED "processYamls"
    FIXTURES_SETUP  "checkGeneratorDatacards_${generator}"
)
endfunction()

foreach(generator ${generatorList})
  check_generator_datacards( ${generator} )
endforeach()


# third test running the generators (define the function first then call it
function(add_generator_run name generator)
  add_test(NAME ${name}_${generator} COMMAND ${RUN_GENERATORS} -g ${generator} )
  set_tests_properties(${name}_${generator}
    PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    ENVIRONMENT ${TEST_ENVIRONMENT}
    TIMEOUT ${TEST_TIMEOUT}
    FIXTURES_REQUIRED "checkGeneratorDatacards_${generator}"
  )
endfunction()

foreach(generator ${generatorList})
  add_generator_run(Run ${generator} )
endforeach()

# thirs test (after all others have been run: gather the xsections
add_test(NAME xsectionRuns COMMAND ${RUN_SUMMARY} )
set_tests_properties("xsectionRuns"
    PROPERTIES
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      ENVIRONMENT ${TEST_ENVIRONMENT}
      DEPENDS "${RunList}"
)

#add_test(NAME Finalize COMMAND ${CMAKE_BINARY_DIR}/bin/eventGenerationSummary -f ${CMAKE_SOURCE_DIR}/test/xsectionSummary.dat)
