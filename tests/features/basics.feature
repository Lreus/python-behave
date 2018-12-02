Feature: showing off behave

  Scenario: run a simple test
    Given we have behave installed
    When we implement a test
    Then behave will test it for that

  Scenario: Expecting the context response as a string
    Given we set the context response to the word "hello"
    Then the context response should be "hello"
    Then the context response length should be 5

  Scenario: allocate some text to context.text attribute
    Given we store the following text
    """
    This text can be written
    on several lines because
    of the triple double quotes.
    """
    Then the context text attribute should contain the word "several"

  Scenario: Count array elements
    Given a set of frameworks
      |name   |language  |
      |flask  |python    |
      |django |python    |
      |symfony|php       |
      |angular|javascript|
      |react  |javascript|
    Then the number of framework should be 5
    And the number of "python" frameworks should be 2
    And the number of "javascript" frameworks should be 2
    And the number of "php" frameworks should be 1