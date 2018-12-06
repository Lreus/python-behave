from sample.classes.simple_class import SimpleClass
from sample.classes.subclasses.simple_subclass import SimpleSubClass
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
