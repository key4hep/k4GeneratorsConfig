# generl settings:
set(TEST_ENVIRONMENT "PATH=${PROJECT_BINARY_DIR}/bin:$ENV{PATH}")
set(TEST_TIMEOUT 3500)

# we split the execution into four steps:
set(EXECUTABLE "${PROJECT_SOURCE_DIR}/python/k4GeneratorsConfig.py")

# the generators to be run
set(generatorList Babayaga KKMC Madgraph Pythia Sherpa Whizard )

# generate the run list for the dependencies
foreach(generator ${generatorList})
  list(APPEND RunList Run_${generator})
  message(${generator} " appended to the runlist ")
endforeach()

# add the first test: setting up the yaml files
add_test(NAME createGeneratorDatacards COMMAND python3 ${EXECUTABLE} --make --outputDir Run-Cards )
set_tests_properties("createGeneratorDatacards"
  PROPERTIES
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  ENVIRONMENT ${TEST_ENVIRONMENT}
  FIXTURES_SETUP  "processYamls"
)

# add the second test: comparing the yaml files to the reference files
function(check_generator_datacards generator)
  add_test(NAME checkGeneratorDatacards_${generator} COMMAND python3 ${EXECUTABLE} --check  --generator ${generator}  --outputDir Run-Cards )
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
  add_test(NAME ${name}_${generator} COMMAND python3 ${EXECUTABLE} --generate  --generator ${generator}  --outputDir Run-Cards )
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

# third test (after all others have been run: gather the xsections
add_test(NAME xsectionRuns COMMAND python3 ${EXECUTABLE} --summary  --outputDir Run-Cards )
set_tests_properties("xsectionRuns"
    PROPERTIES
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      ENVIRONMENT ${TEST_ENVIRONMENT}
      DEPENDS "${RunList}"
)
