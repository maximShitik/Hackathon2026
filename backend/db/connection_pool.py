from abc import ABC, abstractmethod
from contextlib import contextmanager
from backend.db.database_connection import DatabaseConnection


class ConnectionPool(ABC):
    """
    Interface implemented by objects providing DB connection pools.
    """

    @abstractmethod
    def get_connection(self) -> DatabaseConnection:
        """
        Borrow a connection from the pool.

        :return: A connection to the database.
        """
        pass

    @abstractmethod
    def return_connection(self, conn: DatabaseConnection) -> None:
        """
        Return the given connection to the pool.

        :param conn: The connection to return.
        """
        pass

    @contextmanager
    def connection(self):
        """
        A context manager wrapper for borrow/return logic.
        """
        conn = self.get_connection()
        try:
            yield conn
        finally:
            self.return_connection(conn)
