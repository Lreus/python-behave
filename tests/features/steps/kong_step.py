from behave import *
import requests
import json


@Given('kong is accessible at "{url}"')
def kong_is_accessible(context, url: str = '') -> None:
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
    code_error = 'No api answered at {url} with a status code 200'.format(url=url)
    assert isinstance(response, requests.Response), api_error
    assert response.status_code == 200, ' '.join((code_error, response.status_code, 'was returned'))

    response_content = json.loads(response.content)
    assert ('tagline' in response_content and response_content['tagline'] == 'Welcome to kong'), \
        'Unable to find tagline "Welcome to kong" in response json content'
    context.kong_url = url


@Given('there is no service named "{service_name}"')
def there_is_no_service(context, service_name: str = '') -> None:
    url = ''.join((context.kong_url, '/services/', service_name, '/'))
    response = requests.get(url)
    assert response.status_code == 404, 'Unexpected status code '.join(response.status_code)

#When I create a service named "my-custom-service"
#And I request kong for service "my-custom-service"
#Then the response status code should be 200
#And the response content should contain Json

