from behave import *
from manager.postgre_context_manager import PostGreContextManager

from behave.runner import Context
from behave.model import Table

@Given('kong database is accessible over this psql configuration')
def set_kong_database(context: Context) -> None:
    """set_kong_database

    Behave step  Given kong_database is accessible over this psql configuration
    Check and store configuration parameters to kong database with parameters
    provided in context.table

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
