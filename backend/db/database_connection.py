"""
This module exposes abstractions used for database connections.

Classes:
    IDictCursor: Protocol for cursors returning dictionaries.
    DatabaseConnection: Abstract class for database connections following PEP 249.
"""

from abc import ABC, abstractmethod
from typing import Protocol, Any, Dict, List, Optional, Iterable, Sequence


class IDictCursor(Protocol):
    """
    Protocol implemented by objects operating as PEP 249 DB cursors and returning a 
    python dictionary as an execution or fetch result.
    """
    description: Optional[Sequence[Any]]
    rowcount: int

    def execute(self, sql: str, params: Any = ...) -> 'IDictCursor':
        """
        Execute a SQL query.
        """
        ...

    def executemany(self, sql: str, seq_of_params: Iterable[Any]) -> 'IDictCursor':
        """
        Execute a SQL query multiple times.
        """
        ...

    def fetchone(self) -> Optional[Dict[str, Any]]:
        """
        Fetch the next row of a query result, returning a single sequence, or None when no more
        data is available.
        """
        ...

    def fetchmany(self, size: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetch the next set of rows of a query result, returning a list.
        """
        ...

    def fetchall(self) -> List[Dict[str, Any]]:
        """
        Fetch all (remaining) rows of a query result, returning them as a list.
        """
        ...

    def close(self) -> None:
        """
        Close the cursor.
        """
        ...

    def __iter__(self) -> Iterable[Dict[str, Any]]:
        """
        Return an iterator over the rows of a query result.
        """
        ...


class DatabaseConnection(ABC):
    """
    Interface implemented by objects that represent a database connection, in 
    compliance with the Python Database API Specification v2.0 (PEP 249).
    """

    @abstractmethod
    def cursor(self) -> IDictCursor:
        """
        Return a new Cursor object.
        """
        ...

    @abstractmethod
    def commit(self):
        """
        Commit pending transactions.
        """
        ...

    @abstractmethod
    def rollback(self):
        """
        Roll back pending transactions.
        """
        ...

    @abstractmethod
    def begin(self, modifiers: Optional[str]=None):
        """
        Begin a transaction.
        """
        ...

    @abstractmethod
    def close(self):
        """
        Close the database connection.
        """
        ...

    ### Context management block. ###
    def __enter__(self):
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handle context management.
        """
        ...
