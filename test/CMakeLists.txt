add_test(NAME input_checks COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/inputCheck.sh)
set_tests_properties(input_checks
  PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
add_test(NAME run_checks COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/runCheck.sh)
set_tests_properties(run_checks
  PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    ENVIRONMENT "CONVERTHEPMC2EDM4HEP=${PROJECT_BINARY_DIR}/bin"
)
add_test(NAME clean_checks COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/cleanCheck.sh)
set_tests_properties(clean_checks
  PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
