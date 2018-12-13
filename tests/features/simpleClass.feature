Feature: Test a simple class out of the test directory

  Scenario: Say hello and receive a wave
    Given I have a simple class
    When I say hello
    Then the class should wave

  Scenario: Assert about inheritance of a class
    Given I have a simple subclass
    Then the subclass shall inherit from "SimpleClass"


  Scenario Outline: Assert about an internet request with urllib
    Given I call the url "<url>"
    Then the response status code should be <code>

  Examples:
    |url                        |code|
    |http://www.google.com/hello|404 |
    |http://www.google.com      |200 |
    |https://www.google.com     |200 |

  Scenario Outline: Assert about an internet request with requests module
    Given i call the <url> with method <method>
    Then the request response status code should be <code>

  Examples:
    |url                        |method|code|
    |http://www.google.com/hello|GET   |404 |
    |http://www.google.com      |GET   |200 |
    |https://www.google.com     |GET   |404 |