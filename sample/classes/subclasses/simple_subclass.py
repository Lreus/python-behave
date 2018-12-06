from ..simple_class import SimpleClass


class SimpleSubClass(SimpleClass):
    """SimpleSubClass

    Class extending the class SimpleClass
    """
    def hello(self):
        """hello()

        :return: a simple string 'hi'
        :rtype: str
        """
        return 'hi'
