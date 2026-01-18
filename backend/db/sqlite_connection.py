"""
This module exposes classes and functions for interacting with the
 SQLite database.

Classes:
    SQLiteWrapper: A wrapper for a SQLite connection that implements
     the DatabaseConnection interface.

Functions:
    get_db: Returns a connection to the SQLite database.
"""
import sqlite3
import os
from typing import Optional
from backend.db.database_connection import DatabaseConnection
from backend.db.dict_cursor import DictCursor


class SQLiteWrapper(DatabaseConnection):
    """
    A wrapper for a SQLite connection that implements the
    DatabaseConnection interface.
    """

    def __init__(self, db_path: str, **kwargs):
        self._conn = sqlite3.connect(db_path, **kwargs)

    def cursor(self):
        return DictCursor(self._conn.cursor())

    def begin(self, modifiers: Optional[str] = "IMMEDIATE"):
        self._conn.execute(f"BEGIN {modifiers if modifiers is not None else ''};")

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Rollback if an exception was raised, otherwise commit.

        :param exc_type: The type of the exception.
        :param exc_val: The exception value, Unused.
        :param exc_tb: The exception traceback, Unused.
        """
        if exc_type is not None:
            self._conn.rollback()
        else:
            self._conn.commit()


def get_db(db_path="pharmacy.db") -> DatabaseConnection:
    """
    :param db_path: The path to the SQLite database.
    :return: A connection to the SQLite database.
    """
    conn = SQLiteWrapper(db_path, check_same_thread=False)
    conn.cursor().execute("PRAGMA foreign_keys = ON;")
    return conn
