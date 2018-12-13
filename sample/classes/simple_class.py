from urllib.request import urlopen, Request
from urllib.error import URLError
import requests
import logging


class SimpleClass:
    """SimpleClass

    A simple class to be tested by features localized in tests/features
    """
    def hello(self) -> str:
        """hello()
        :return: a simple string: 'wave'
        :rtype: str
        """
        return 'wave'

    @staticmethod
    def go_to_url(url: str, method: str):
        """go_to_url()

        Reaches an url with the given method and return the client response
        or the URLError that might occur.

        :return: http.client.HTTPResponse | urllib.error.URLError
        :rtype: object
        """
        request = Request(url=url, method=method)
        try:
            return urlopen(request)
        except URLError as error:
            return error

    @staticmethod
    def go_to_request(url: str, method: str):
        """go_to_request()

        Perform an http request with the very popular Requests module.
        Requests is very efficient at building easily complex requests.
        see http://docs.python-requests.org/en/master/.

        :param url: string of valid url including schema
        :param method: string of HTTP method
        :return:
        """
        try:
            return requests.request(method, url)
        except Exception as error:
            logging.critical(
                'Calling {url} with method {method} raised an unhandled exceptions : {Eclass}' \
                .format(url=url, method=method, Eclass=error.__class__)
            )
            return None
