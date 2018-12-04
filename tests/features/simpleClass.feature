Feature: Test a simple class out of the test directory

  @wip
  Scenario: Say hello and receive a wave
    Given I have a simple class
    When I say hello
    Then the class should wave