from sample.classes.simple_class import SimpleClass
from sample.classes.subclasses.simple_subclass import SimpleSubClass
from urllib.error import URLError, HTTPError
from http.client import HTTPResponse

from behave import *


def class_mapping():
    """

    :return:
    :rtype: dict
    """
    return {
        'SimpleClass': SimpleClass,
        'SimpleSubClass': SimpleSubClass,
    }


@Given('I have a simple class')
def i_have_a_simple_class(context):
    context.simpleClass = SimpleClass()


@When('I say hello')
def i_say_hello(context):
    context.response = context.simpleClass.hello()


@Then('the class should wave')
def class_should_wave(context):
    assert context.response == 'wave'


@Given('I have a simple subclass')
def i_have_a_simple_subclass(context):
    context.Class = {'subclass': SimpleSubClass()}


@Then('the subclass shall inherit from "{class_name}"')
def the_subclass_shall_inherit_from(context, class_name):
    try:
        mapped_class = class_mapping()[class_name]
    except KeyError:
        print('available class to test are', [k for k in class_mapping()])
        raise AssertionError

    assert issubclass(
        type(context.Class['subclass']),
        mapped_class
    )


@Given('I call the url "{url}"')
def i_call_the_url(context, url):
    context.response = SimpleClass.go_to_url(url, "GET")


@Then('the response status code should be {code:d}')
def status_code_is(context, code):
    assert isinstance(context.response, (HTTPResponse, HTTPError)), \
        "context.response is neither an HTTPResponse nor an HTTPError: %r" % context.response.__class__

    assert context.response.code == code, \
        "context response does not match 200: %r " % context.response.code

