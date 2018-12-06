from behave import *
"""basics.py

Commented test examples based on behave documentation
"""


@given('we have behave installed')
def empty_method(context):
    """
        Even if it may not be used, context argument is required for step
        implementation methods. It is an instance of behave.runner.Context
    """
    pass


@when('we implement a test')
def assert_obvious(context):
    """
        A failed assertion will raise an exception and therefore make the test fail
        if it has not been caught
    """
    assert True is not False


@then('behave will test it for that')
def check_context(context):
    assert context.failed is False


@given('we store the following text')
def set_text_block_to_response(context):
    """
        The decorator will allocate the content of a following text block
        (delimited by three double quotes) to context.text attribute
    """
    context.response = context.text


@given('we set the context response to the word "{word}"')
def set_string_to_response(context, word):
    """
        the Formatted String Literals syntax {}, allows us to allocate a variable
        string from the step definition to an attribute.

        context.response is the recommended attribute but it is not mandatory

         https://behave.readthedocs.io/en/latest/api.html#behave.runner.Context
         lists the attribute managed by behave. It is not advised to overwrite
         them.
         Examples:
        - context.table
        - context.text
        - context.failed
        - ...
    """
    context.response = word
    context.random = word


@then('the context response should be "{text}"')
def is_equal_to_response(context, text):
    """
        a previously allocated context attribute is accessible through multiple steps.
    """
    assert text == context.response
    assert text == context.random


@then('the context response length should be {number:d}')
def response_length(context, number):
    """
        the syntax 'name:type' allows to define type variable and restrict the step to
        this type.
        This step won't be triggered if number is not an integer
    """
    assert number == len(context.response)


@then('the context text attribute should contain the word "{text}"')
def does_response_contain(context, text):
    """
        Search for the given word in context response
    """
    assert text in context.response


@given('a set of frameworks')
def store_framework_table(context):
    """
        A two dimensional array can be provided as a variable. It will be available
        in the context.table attribute.
    """
    context.response = context.table


@then('the number of framework should be {number:d}')
def is_equal_to_total_framework(context, number):
    """
        A context.table attribute is a behave.model.Table.
        It contains rows of key/value elements.
        The keys are defined in the first row.
        Table.rows method returns a list of behave.model.Row
    """
    assert len(context.response.rows) == number


@then('the number of "{language}" frameworks should be {number:d}')
def time_language_appears(context, language, number):
    """
        behave.model.Row class allows the syntax data = row[key]
        but they are not dictionaries !
    """
    occurrences = {}
    for row in context.response.rows:
        lang = row['language']
        if lang in occurrences:
            occurrences[lang] = occurrences[lang] + 1
        else:
            occurrences[lang] = 1
    assert occurrences[language] == number