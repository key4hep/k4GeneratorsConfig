add_test(NAME basic_checks COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/check.sh)
set_tests_properties(basic_checks
  PROPERTIES
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
