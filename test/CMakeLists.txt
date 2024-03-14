add_test(NAME input_check COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/inputCheck.sh)
set_tests_properties(input_check
  PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
add_test(NAME run_check COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/runCheck.sh)
set_tests_properties(run_check
  PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    ENVIRONMENT "CONVERTHEPMC2EDM4HEP=${PROJECT_BINARY_DIR}/bin"
)
add_test(NAME clean_check COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/cleanCheck.sh)
set_tests_properties(clean_check
  PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
set_tests_properties(input_check PROPERTIES COST 100)
set_tests_properties(run_check   PROPERTIES COST 10)
set_tests_properties(clean_check PROPERTIES COST 1)
