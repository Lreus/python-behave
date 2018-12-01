from behave import *
"""
    Commented examples based on behave documentation
"""
context_text = ''


@given('we have behave installed')
def step_impl(context):
    """
        Even if it may not be used, context argument is required for step
        implementation methods
    """
    pass


@when('we implement a test')
def step_impl(context):
    """
        A failed assertion will raise an exception and therefore make the test fail
        if it has not been caught
    """
    assert True is not False


@then('behave will test it for that')
def step_impl(context):
    assert context.failed is False


@given('we store the following text')
def step_impl(context):
    """
        The decorator will allocate the content of the following text block
        to context.text attribute
    """
    context.response = context.text


@given('we set the context response to the word "{word}"')
def step_impl(context, word):
    """
        the syntax {} allows us to set a word from the step to a parameter
    """
    context.response = word


@then('the context response should be "{text}"')
def step_impl(context, text):
    """
        a previously allocated context response is accessible through multiple steps
    """
    assert text == context.response


@then('the context text attribute should contain the word "{text}"')
def step_impl(context, text):
    """
        Search for the given word in context response
    """
    assert text in context.response.split()
