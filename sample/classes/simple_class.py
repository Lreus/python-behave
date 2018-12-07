from urllib.request import urlopen, Request
from urllib.error import URLError


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
