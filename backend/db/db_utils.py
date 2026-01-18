"""
This model exposes utility functions for database interactions.

Functions:
    execute_sql_script: Executes a multi-statement SQL script on 
    any PEP 249 DatabaseConnection, committing the transaction if commit is 
    True.
"""
from backend.db.database_connection import DatabaseConnection
from typing import List


def execute_sql_script(connection: DatabaseConnection, script: str, commit: bool = True) -> None:
    """
    Executes a multi-statement SQL script on any PEP 249 DatabaseConnection, 
    committing the transaction if commit is True.
    
    :param connection: The database connection.
    :param script: The SQL script to execute.
    :param commit: Whether to commit the transaction.
    """
    statements = split_sql_script(script)
    cursor = connection.cursor()
    for statement in statements:
        clean_statement = statement.strip()
        if clean_statement:
            cursor.execute(clean_statement)
    if commit:
        connection.commit()


def split_sql_script(script: str) -> List[str]:
    """
    Splits the given SQL script into a list of queries.
    :param script: The script to be split
    :return: list of containing queries defined in the given script.
    """
    return [query.strip() + ';' for query in script.split(';') if query.strip()]
