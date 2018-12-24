from behave import *
from manager.postgre_context_manager import PostGreContextManager

from behave.runner import Context
from behave.model import Table


@Given('kong database is accessible over this psql configuration')
def set_kong_database(context: Context) -> None:
    """set_kong_database

    Behave step  Given kong_database is accessible over this psql configuration
    Check and store configuration parameters to kong database with parameters
    provided in context.table.

    :param context: Behave context manager
    :type context: Context

    :rtype: None
    """
    context.table: Table

    kong_db_config = {key: value for key, value in context.table.rows}

    with PostGreContextManager(kong_db_config) as cursor:
        query = 'SELECT * from services;'
        cursor.execute(query)
        results = cursor.fetchall()

    if isinstance(results, list):
        context.kong_db_config = kong_db_config


@Given('I delete all oauth2 credentials')
def i_delete_oauth2_credentials(context: Context) -> None:
    """i_delete_oauth2_credentials

    Behave step Given I delete all oauth2_credentials.
    Part of the kong database cleanup process.
    Clear the table oauth2_credentials.

    Expect to found context.kong_db_config attribute providing database
    credentials.

    :param context: Behave context manager
    :type context: Context

    :rtype: None
    """
    context.kong_db_config: dict
    with PostGreContextManager(context.kong_db_config) as cursor:
        query = 'DELETE FROM oauth2_credentials;'
        cursor.execute(query)


@Given('I delete all plugins')
def i_delete_plugins(context: Context) -> None:
    """i_delete_plugins

    Behave step Given I delete all plugins.
    Part of the kong database cleanup process.
    Clear the table plugins.

    Expect to found context.kong_db_config attribute providing database
    credentials.

    :param context: Behave context manager
    :type context: Context

    :rtype: None
    """
    context.kong_db_config: dict
    with PostGreContextManager(context.kong_db_config) as cursor:
        query = 'DELETE FROM plugins;'
        cursor.execute(query)


@Given('I delete all consumers')
def i_delete_consumers(context: Context) -> None:
    """i_delete_consumers

    Behave step Given I delete all consumers.
    Part of the kong database cleanup process.
    Clear the table consumers.

    Expect to found context.kong_db_config attribute providing database
    credentials.

    :param context: Behave context manager
    :type context: Context

    :rtype: None
    """
    context.kong_db_config: dict
    with PostGreContextManager(context.kong_db_config) as cursor:
        query = 'DELETE FROM consumers;'
        cursor.execute(query)


@Given('I delete all services')
def i_delete_services(context: Context) -> None:
    """i_delete_services

    Behave step Given I delete all services.
    Part of the kong database cleanup process.
    Clear the table services.

    Expect to found context.kong_db_config attribute providing database
    credentials.

    :param context: Behave context manager
    :type context: Context

    :rtype: None
    """
    context.kong_db_config: dict
    with PostGreContextManager(context.kong_db_config) as cursor:
        query = 'DELETE FROM services;'
        cursor.execute(query)
