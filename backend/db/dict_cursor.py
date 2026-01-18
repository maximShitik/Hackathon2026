from typing import Any, Dict, List, Optional, Iterable, Sequence
from backend.db.database_connection import IDictCursor


class DictCursor(IDictCursor):
    """
    A wrapper for PEP 249 cursors that ensures all fetch  operations return 
    dictionaries instead of tuples.
    """
    def __init__(self, real_cursor: Any):
        """
        Initializes the wrapper with the given cursor.

        :param real_cursor: The cursor to wrap.
        """
        self._cursor = real_cursor

    @property
    def description(self) -> Optional[Sequence[Any]]:
        """
        :return: The description of the cursor.
        """
        return self._cursor.description

    @property
    def rowcount(self) -> int:
        """
        :return: The number of rows affected by the last operation.
        """
        return self._cursor.rowcount

    def execute(self, sql: str, params: Any = ()) -> 'DictCursor':
        """
        Executes the given SQL statement.

        :param sql: The SQL statement to execute.
        :param params: The parameters to pass to the SQL statement.
        :return: The cursor.
        """
        self._cursor.execute(sql, params)
        return self

    def executemany(self, sql: str, seq_of_params: Iterable[Any]) -> 'DictCursor':
        """
        Executes the given SQL statement multiple times.

        :param sql: The SQL statement to execute.
        :param seq_of_params: The parameters to pass to the SQL statement.
        @return: The cursor.
        """
        self._cursor.executemany(sql, seq_of_params)
        return self

    def _row_to_dict(self, row: Optional[Sequence[Any]]) -> Optional[Dict[str, Any]]:
        """
        Helper to convert a single tuple row into a dictionary.

        :param row: The row to convert.
        @return: The dictionary.
        """
        if row is None:
            return None
        column_names = [col[0] for col in self._cursor.description]
        return dict(zip(column_names, row))

    def fetchone(self) -> Optional[Dict[str, Any]]:
        """
        Fetches the next row of a query result, returning a dictionary, or None when no 
        more data is available.

        @return: The next row of a query result, or None when no more data is available.
        """
        row = self._cursor.fetchone()
        return self._row_to_dict(row)

    def fetchmany(self, size: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetches the next set of rows of a query result, returning a list.

        :param size: The number of rows to fetch.
        @return: The next set of rows of a query result, or an empty list if no more data
        is available.
        """
        rows = self._cursor.fetchmany(size) if size is not None else self._cursor.fetchmany()
        return [self._row_to_dict(row) for row in rows]

    def fetchall(self) -> List[Dict[str, Any]]:
        """
        Fetches all rows of a query result, returning a list.

        @return: The list of rows of a query result, or an empty list if no more data is
        available.
        """
        rows = self._cursor.fetchall()
        return [self._row_to_dict(row) for row in rows] 

    def close(self) -> None:
        """
        Closes the cursor.
        """
        self._cursor.close()

    def __iter__(self) -> Iterable[Dict[str, Any]]:
        """
        Allows: for row in cursor: ...
        """
        for row in self._cursor:
            yield self._row_to_dict(row) 

    def __getattr__(self, name: str) -> Any:
        """
        Forward any non-standard methods to the underlying cursor.
        """
        return getattr(self._cursor, name)
