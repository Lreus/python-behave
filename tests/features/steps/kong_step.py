from behave import *

from behave.runner import Context
from behave.model import Table
from requests import Response
from typing import List

import requests
import json


def build_unexpected_code_message(
        expected_code: List[int],
        received_code: int
) -> str:
    """build_unexpected_code_message(expected_code: int, received_code: int)

    :param expected_code: The expected http code
    :param received_code: The received http code

    :return: Error message formatted with parameters

    :rtype: str
    """
    return 'Unexpected status code: {got} while expecting {expectation} '\
        .format(
            got=received_code,
            expectation=' or '.join(str(code) for code in expected_code))


def context_has_valid_response(context: Context = None) -> bool:
    """context_has_valid_response(context: Context= None)

    Assert context has an attribute 'response' and that it contains
    a requests.Response object

    :param context: behave context manager
    :type context: Context

    :return: True if all assertions were successful
    :rtype: bool

    :raise: AssertionError
    """
    assert hasattr(context, 'response') and context.response is not None,\
        'No response attribute set in context manager'

    assert isinstance(context.response, Response), \
        'Attribute response in context manager contains {class_name}'\
        .format(class_name=context.response.__class__)

    return True


@Given('kong is accessible at "{url}"')
def kong_is_accessible(context: Context, url: str = '') -> None:
    """kong_is_accessible

    Behave background step: Given kong is accessible at "{url}".
    Requests the provided url and expects a Json response.
    Search for kong tagline in response.
    Stores url parameter in context.kong_url attribute on success.

    :param context: Behave context object
    :type context: behave.runner.Context

    :param url: The url needed use to contact kong api
    :type url: str

    :rtype: None

    :raise: AssertionError
    """
    response = requests.get(url)
    api_error = 'No api answered at {url} with a status code 200'\
        .format(url=url)

    assert isinstance(response, requests.Response), api_error
    assert response.status_code == 200, build_unexpected_code_message(
        [200],
        response.status_code)

    response_content = json.loads(response.content)

    assert (
            'tagline' in response_content
            and response_content['tagline'] == 'Welcome to kong'
    ), 'Unable to find tagline "Welcome to kong" in response json content'

    context.kong_url = url


@Given('there is no service named "{service_name}"')
def there_is_no_service(context: Context, service_name: str = '') -> None:
    """there_is_no_service

    Behave background step: Given there is no service named "{service_name}".
    Request the provided service name to kong api.
    If the service exists call step 'Given i delete the service' and perform a
    new request.
    Expects the response status code 404 Not found.
    Uses context.kong_url string initialized in kong_is_accessible background
    test.

    :param context: Behave context object
    :type context: behave.runner.Context

    :param service_name: the name of the expected missing service
    :type service_name: str

    :rtype: None

    :raise: AssertionError
    """
    context.kong_url: str

    url = ''.join((context.kong_url, '/services/', service_name, '/'))
    response = requests.get(url)

    if response.status_code == 200:
        # If the service already exists (maybe from a previous test suite)
        # Execute the test suite to delete it and perform another call
        context.execute_steps(u'''
            Given i delete the service "{service_name}"
        '''.format(service_name=service_name))
        response = requests.get(url)

    assert response.status_code == 404, build_unexpected_code_message(
        [404],
        response.status_code)


@When('I create a service named "{service_name}" pointing to "{service_url}"')
def i_create_service(
        context: Context,
        service_name: str = '',
        service_url: str = ''
) -> None:
    """i_create_service

    Behave background step: When I create a service named "{service_name}".
    Request kong to create a service with the provided name.
    Expects the response to be a 201 Created.
    Uses context.kong_url string initialized in kong_is_accessible background
    test.

    :param context: Behave context object
    :type context: behave.runner.Context

    :param service_name: the name of the expected missing service
    :type service_name: str

    :param service_url: the url pointed by the new kong service
    :type service_url: str

    :rtype: None

    :raise: AssertionError
    """
    context.kong_url: str

    url = ''.join((context.kong_url, '/services/'))
    post_data = {
        'name': service_name,
        'url': service_url
    }
    response = requests.post(url, post_data)

    assert response.status_code == 201, build_unexpected_code_message(
        [201],
        response.status_code)


@Given('I delete the service "{service_name}"')
def i_delete_service(context: Context, service_name: str = '') -> None:
    """i_delete_service

    Behave background step: Given I delete the service "{service_name}".
    Request kong to delete a service named with the provided name.
    Expects the response to be a 204 No content.
    Uses context.kong_url string initialized in kong_is_accessible background
    test.

    :param context: Behave context object
    :type context: behave.runner.Context

    :param service_name: the name of the expected missing service
    :type service_name: str

    :rtype: None

    :raise: AssertionError
    """
    context.kong_url: str

    url = ''.join((context.kong_url, '/services/', service_name, '/'))
    response = requests.delete(url)

    assert response.status_code == 204, build_unexpected_code_message(
        [204],
        response.status_code)


@When('I request kong for service "{service_name}"')
def i_request_service(context: Context, service_name: str = '') -> None:
    """i_request_service

    Behave background step: When I request kong for service "{service_name}".
    Request kong for a service named with provided parameter
    Store response in context.response attribute.
    Uses context.kong_url string initialized in kong_is_accessible background
    test.

    :param context: Behave context object
    :type context: behave.runner.Context

    :param service_name: the name of the required service
    :type service_name: str

    :rtype: None

    :raise: AssertionError
    """
    context.kong_url: str

    url = ''.join((context.kong_url, '/services/', service_name, '/'))

    context.response = requests.get(url)


@Then('the request status code should be {code:d}')
def request_code_equals(context: Context, code: int) -> None:
    """request_code_equals

    Behave background step: Then the request status code should be {code:d}.
     and that it's
    Uses context_has_valid_response to validate context response.
    status_code attribute matches code parameter.

    :param context: Behave context object
    :type context: Context

    :param code: Integer matching an HTTP status code
    :type code: int

    :rtype: None

    :raise: AssertionError
    """
    if context_has_valid_response(context):
        assert context.response.status_code == code, \
            build_unexpected_code_message([200], context.response.status_code)


@Then('the response content should contain JSON')
def is_response_json(context: Context):
    """is_response_json

    Behave background step: Then the response content should contain JSON
    Uses context_has_valid_response to validate context response.
    Decode as Json the context.response.content and saves it in
    context.json_response.

    :param context: Behave context object
    :type context: Context

    :rtype: None

    :raise: AssertionError
    """
    if context_has_valid_response(context):
        context.json_response = json.loads(context.response.content)


@Then('the response should have the matching key-values pairs')
def response_contain_key_value(context: Context) -> None:
    """response_contain_key_value

    Behave background step: Then the response should have the matching
    key-values pairs.
    Validate that the context manager has an attribute json_response.
    Check if each key/value pair from the provided context table appears in
    context.json_response.

    :param context: Behave context object
    :type context: Context

    :rtype: None

    :raise: AssertionError
    """
    context.table: Table
    assert hasattr(context, 'json_response') \
        and context.json_response is not None, \
        'No json_response attribute in context manager'

    assert isinstance(context.json_response, dict), \
        'context.json_response is not a dict but a {class_name}'\
        .format(class_name=context.json_response.__class__)

    assert 'key' in context.table.headings,\
        'Please use the word "key" as first column header for this step'

    assert 'value' in context.table.headings,\
        'Please use the word "value" as first column header for this step'

    for row in context.table.rows:
        assert row['key'] in context.json_response,\
            'Unable to find key {key} in json response'.format(key=row['key'])

        incoming_value = context.json_response[row['key']]
        assert row['value'] == str(incoming_value), \
            '''
            Unexpected value for json_response["{key}"] got {unexpected} 
            <{unexpected_class}> while expecting {value} <{class_name}>
            '''.format(
                key=row['key'],
                unexpected=context.json_response[row['key']],
                unexpected_class=context.json_response[row['key']].__class__,
                value=row['value'],
                class_name=row['value'].__class__
            )


@When('I create a consumer named "{username}" with id "{custom_id}"')
def i_create_consumer(
        context: Context,
        username: str = '',
        custom_id: str = ''
) -> None:
    """there_is_a_consumer_identified_by

        Behave background step: When I create a consumer named "{username}"
        with id "{custom_id}".
        Creates a consumer.

        Uses context.kong_url string initialized in kong_is_accessible
        background test.

        :param context: Behave context object
        :type context: Context

        :param username: The consumer Username
        :type username: str

        :param custom_id: The consumer custom id
        :type custom_id: str

        :rtype: None

        :raise: AssertionError
        """
    context.kong_url: str
    user = {
        'username': username,
        'custom_id': custom_id,
    }

    url = ''.join((context.kong_url, '/consumers/'))
    response = requests.post(url, user)

    assert response.status_code == 201, build_unexpected_code_message(
        [201],
        response.status_code)


@Given('there is a consumer identified by')
def there_is_a_consumer_identified_by(context: Context) -> None:
    """there_is_a_consumer_identified_by

    Behave background step: Given there is a consumer identified by.
    Ensure a consumer exists in kong service.
    Attempt to get the consumer with provided credentials in
    context.Model.Table.

    Execute consumer creation step if the consumer is not found.
    Perform a second Call to store the consumer id.
    Uses context.kong_url string initialized in kong_is_accessible background
    test.

    :param context: Behave context object
    :type context: Context

    :rtype: None

    :raise: AssertionError
    """
    context.table: Table
    context.kong_url: str

    assert 'username' in context.table.headings,\
        'Please use the word "username" as first column header for this step'

    assert 'custom_id' in context.table.headings,\
        'Please use the word "custom_id" as first column header for this step'

    user = {
        'username': context.table.rows[0]['username'],
        'custom_id': context.table.rows[0]['custom_id'],
    }

    url = ''.join((context.kong_url, '/consumers/', user['username']))

    response = requests.get(url)

    assert response.status_code in [404, 200], build_unexpected_code_message(
        [404, 200],
        response.status_code)

    if response.status_code == 404:
        context.execute_steps(u'''
            When I create a consumer named "{username}" with id "{custom_id}"
            '''.format(**user)
        )
        response = requests.get(url)

    assert response.status_code == 200, build_unexpected_code_message(
        [200],
        response.status_code)
