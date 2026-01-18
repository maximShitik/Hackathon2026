"""
This module exposes the initialization of the database.

Functions:
    init_db_if_needed: Initialize the database if it doesn't exist at the path specified in its
    db_path_str parameter, defaulting to ./pharmacy.db if the variable is not set. 
    Applies the schema as defined in the schema.sql file, and populates the DB 
    using the seed.sql file.
"""

import os
from pathlib import Path
from typing import Callable
from backend.db.db_utils import execute_sql_script
from backend.db.database_connection import DatabaseConnection
from db.queries import CHECK_DB_EXISTS


def init_db_if_needed(connection_factory: Callable[[], DatabaseConnection],
                      db_path_str="pharmacy.db") -> None:
    """
    Initialize the database if it doesn't exist at the path specified in its
    db_path_str parameter, defaulting to ./pharmacy.db if the variable is not set. 
    Applies the schema as defined in the schema.sql file, and populates the DB 
    using the seed.sql file.

    :param connection_factory: Function that creates the database connection.
    :param db_path_str: String representing the path to initialize the database at.
    """
    db_path = Path(db_path_str)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = connection_factory()
    if _check_db_exists(conn):
        return

    schema_sql = Path("./db/schema.sql").read_text(encoding="utf-8")
    seed_sql = Path("./db/db_seed.sql").read_text(encoding="utf-8")

    execute_sql_script(conn, schema_sql)
    execute_sql_script(conn, seed_sql)
    conn.commit()


def _check_db_exists(conn: DatabaseConnection) -> bool:
    """
    Check if the database exists by checking if the users table exists
    using the given connection.

    :param conn: The database connection.
    :return: True if the database exists, False otherwise.
    """
    exists = conn.cursor().execute(CHECK_DB_EXISTS).fetchone()
    return exists is not None
