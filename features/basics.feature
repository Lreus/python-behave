Feature: showing off behave

  Scenario: run a simple test
    Given we have behave installed
    When we implement a test
    Then behave will test it for that

  Scenario: Expecting the context response as a string
    Given we set the context response to the word "hello"
    Then the context response should be "hello"

  Scenario: allocate some text to context.text attribute
    Given we store the following text
    """
    This text can be written
    on several lines because
    of the triple double quotes.
    """
    Then the context text attribute should contain the word "several"
