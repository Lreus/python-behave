Feature: showing off behave

  Scenario: run a simple test
    Given we have behave installed
    When we implement a test
    Then behave will test it for that

  Scenario: Expecting the context response as a string
    Given we set the context response to the word "hello"
    Then the context response should be "hello"
    Then the context response length should be 5

  @wip
  Scenario Outline: Scenario outline can repeat the scenario
                    with multiple example
    Given we set the context response to the word "<string>"
    Then the context response should be "<string>"
    Then the context response length should be <number>

    Examples: Single Word
      |string  |number|
      |hello   |5   |
      |warning |7   |
      |error   |5   |

    Examples: Sentences
      |string       |number|
      |hello Ludovic|13    |
      |It's all good|13    |
      |I am fine    |9     |

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