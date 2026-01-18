import threading
from contextlib import contextmanager

from backend.db.database_connection import DatabaseConnection
from backend.db.connection_pool import ConnectionPool


class SingleInstancePool(ConnectionPool):
    """
    A connection pool that keeps a single connection open for the duration of 
    the application, for simplicity.
    It is advised to use 'with pool.connection() as conn:' to get a connection.
    """

    def __init__(self, connection_factory):
        """
        Initializes the pool with the given connection_factory.
        :param connection_factory: A function that returns a connection.
        """
        self._factory = connection_factory
        self._shared_conn = None
        self._lock = threading.Lock()

    def get_connection(self) -> DatabaseConnection:
        """
        :return: The shared connection to the database.
        """
        if self._shared_conn is None:
            self._shared_conn = self._factory()
        return self._shared_conn

    def return_connection(self, conn: DatabaseConnection) -> None:
        """
        Since there is only one connection, do nothing.
        """
        ...

    def close(self) -> None:
        """
        Closes the connection
        """
        self._shared_conn.close()

    @contextmanager
    def connection(self):
        """
        Safely accessing the database through the lock.
        """
        conn = self.get_connection()
        with self._lock:
            yield conn
