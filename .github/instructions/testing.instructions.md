---
description: 'Use these guidelines when generating or updating tests.'
applyTo: tests/**,**/*.test.*,**/*.spec.*
---

# Testing Guidelines for TDD

## Test Conventions

- Write clear, focused tests that verify one behavior at a time
- Use descriptive test names that explain what is being tested and the expected outcome
- Follow the Arrange-Act-Assert (AAA) pattern:
  - **Arrange**: Set up test data and initial state
  - **Act**: Execute the code under test
  - **Assert**: Verify the results match expectations
- Keep tests independent - each test should run in isolation without depending on other tests
- Start with the simplest test case, then add edge cases and error conditions
- Tests should fail for the right reason - verify they catch the bugs they're meant to catch
- Mock external dependencies to keep tests fast and reliable

## Test Naming

- Use names that clearly describe what behavior is being tested
- Include the scenario and expected outcome in the test name
- Example: `test_calculateTotal_withMultipleItems_returnsSum()`
- Avoid vague names like `test_works()` or `test_calculation()`

## Test Structure

- One assertion per test is preferred, but related assertions can be grouped
- Use setup and teardown methods to reduce duplication
- Group related tests using test suites or describe blocks
- Keep test files organized alongside or near source code

## Edge Cases and Error Conditions

- Test boundary conditions (null, empty, zero, max values)
- Test error scenarios and exception handling
- Test with valid and invalid inputs
- Test with different data types when applicable
- Test state transitions and side effects

## Test Quality Principles

- Tests should verify behavior, not implementation details
- Avoid testing private methods directly
- Use data builders or factories for complex test data
- Keep tests deterministic - they should pass/fail consistently
- Avoid sleep() or timing-dependent tests
- Test one thing per test function

## Mocking and Isolation

- Mock external dependencies (APIs, databases, file systems)
- Use stubs for dependencies that aren't being tested
- Verify mock interactions when behavior matters
- Keep mocks simple and focused on the test

## Testing Performance

- Aim for fast test execution (< 100ms per test)
- Use test fixtures to share expensive setup
- Run database tests against in-memory alternatives when possible
- Separate unit tests from integration tests
