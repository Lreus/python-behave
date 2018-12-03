from sample.classes.simple_class import SimpleClass
from behave import *


@Given('I have a simple class')
def i_have_a_simple_class(context):
    context.simpleClass = SimpleClass()


@When('I say hello')
def i_say_hello(context):
    context.response = context.simpleClass.hello()


@Then('the class should wave')
def class_should_wave(context):
    assert context.response == 'wave'
