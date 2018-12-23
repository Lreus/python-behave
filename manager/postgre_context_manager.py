import psycopg2
from psycopg2 import OperationalError, ProgrammingError
from psycopg2.extensions import cursor


class ConnectionException(Exception):
    pass


class SqlException(Exception):
    pass


class PostGreContextManager:
    """PostGreContextManager

    Provide context manager to handle sql queries with PostGreSQL databases
    """
    def __init__(self, conf: dict) -> None:
        """PostGreContextManager(self, conf: dict)

        Load database configuration
        conf parameter is expected to be a dictionary matching
        psycopg2.connect() requirements.
        """
        self.dbconf = conf

    def __enter__(self):
        """__enter__ (self)

        Instantiate and return a new cursor with current database configuration.

        :rtype: cursor
        :raise ConnectionException: when an psycopg2.OperationalError is
                excepted
        """
        try:
            self.conn = psycopg2.connect(**self.dbconf)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            raise ConnectionException(str(err))
        except Exception as err:
            raise Exception(err.__class__)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """__exit__(self, exc_type, exc_val, exc_tb)

        Commit any pending query and close database objects.

        :raise: SqlException when a psycopg2.ProgramingError is excepted
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is ProgrammingError:
            raise SqlException(exc_val)
        if exc_type:
            raise exc_type(exc_val)
