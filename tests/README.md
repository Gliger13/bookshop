# Bookshop Tests

## Context

The tests repository folder contains everything related to tests for testing
the bookstore application.

## Structure

- [bookshop-test-framework](bookshop-test-framework) - core for all test cases,
  provides asserts, fixtures, configs, tools for executing test cases.
- [bookshop-unit-tests](bookshop-unit-tests) - unit tests for bookshop
  application package.
- [bookshop-api-tests](bookshop-api-tests) - tests for Bookshop API.
- [bookshop-ui-tests](bookshop-ui-tests) - tests for Bookshop UI.

## Run

1) To execute any type of tests install [bookshop_test_framework installation guide](bookshop-test-framework/README.md#Installation)
   and activate python virtual environment with installed bookshop test framework.
2) Switch to the desired test type folder, for example to Bookshop API Tests:
```shell
cd bookshop-api-tests
```
3) Run tests with test framework environment variables and options:
```shell
ENV="PRODUCTION" pytest . -m smoke
```
