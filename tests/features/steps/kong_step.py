from behave.runner import Context
from behave import *
from requests import Response
import requests
import json


def build_unexpected_code_message(expected_code: int, received_code: int) -> str:
    """build_unexpected_code_message(expected_code: int, received_code: int)

    :param expected_code: The expected http code
    :param received_code: The received http code

    :return: Error message formatted with parameters

    :rtype: str
    """
    return 'Unexpected status code: {code} while expecting {expectation} '\
        .format(code=received_code, expectation=expected_code)


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
    api_error = 'No api answered at {url} with a status code 200'.format(url=url)

    assert isinstance(response, requests.Response), api_error
    assert response.status_code == 200, build_unexpected_code_message(200, response.status_code)

    response_content = json.loads(response.content)

    assert ('tagline' in response_content and response_content['tagline'] == 'Welcome to kong'), \
        'Unable to find tagline "Welcome to kong" in response json content'

    context.kong_url = url


@Given('there is no service named "{service_name}"')
def there_is_no_service(context: Context, service_name: str = '') -> None:
    """there_is_no_service

    Behave background step: Given there is no service named "{service_name}".
    Request the provided service name to kong api.
    If the service exists call step 'Given i delete the service' and perform a new request.
    Expects the response status code 404 Not found.
    Uses context.kong_url string initialized in kong_is_accessible background test.

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

    assert response.status_code == 404, build_unexpected_code_message(404, response.status_code)


@When('I create a service named "{service_name}" pointing to "{service_url}"')
def i_create_service(context: Context, service_name: str = '', service_url: str = '') -> None:
    """i_create_service

    Behave background step: When I create a service named "{service_name}".
    Request kong to create a service with the provided name.
    Expects the response to be a 201 Created.
    Uses context.kong_url string initialized in kong_is_accessible background test.

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

    assert response.status_code == 201, build_unexpected_code_message(201, response.status_code)


@Given('I delete the service "{service_name}"')
def i_delete_service(context: Context, service_name: str = '') -> None:
    """i_delete_service

    Behave background step: Given I delete the service "{service_name}".
    Request kong to delete a service named with the provided name.
    Expects the response to be a 204 No content.
    Uses context.kong_url string initialized in kong_is_accessible background test.

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

    assert response.status_code == 204, build_unexpected_code_message(204, response.status_code)


@When('I request kong for service "{service_name}"')
def i_request_service(context: Context, service_name: str = '') -> None:
    """i_request_service

    Behave background step: When I request kong for service "{service_name}".
    Request kong for a service named with provided parameter
    Store response in context.response attribute.
    Uses context.kong_url string initialized in kong_is_accessible background test.

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
    Assert context.response contains a requests.Response object and that it's
    status_code attribute matches code parameter.

    :param context: Behave context object
    :type context: Context

    :param code: Integer matching an HTTP status code
    :type code: int

    :rtype: None

    :raise: AssertionError
    """
    context.response: Response
    assert hasattr(context, 'response'), 'No response attribute set in context manager'
    assert isinstance(context.response, Response), \
        'Attribute response in context manager contains {class_name}'.format(class_name=context.response.__class__)
    assert context.response.status_code == code, build_unexpected_code_message(200, context.response.status_code)


# And I request kong for service "my-custom-service"
# Then the response status code should be 200
# And the response content should contain Json

