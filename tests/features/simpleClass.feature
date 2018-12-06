Feature: Test a simple class out of the test directory

  Scenario: Say hello and receive a wave
    Given I have a simple class
    When I say hello
    Then the class should wave

  @wip
  Scenario: Assert about inheritance of a class
    Given I have a simple subclass
    Then the subclass shall inherit from "SimpleClass"