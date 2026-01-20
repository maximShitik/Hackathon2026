"""
This module exposes the tool manager, alongisde the tools mapping to actual functions.

Classes:
    ToolManager: Class that handles tools mapping to actual functions and calling them.
"""
import json
from typing import Any, Callable, Dict, Tuple, Type, Union
from dataclasses import asdict
from backend.tools.schemas import *
from backend.tools.stores import *
from backend.tools.products import *
from backend.tools.ads import *
from backend.db.database_connection import DatabaseConnection
from backend.db.connection_pool import ConnectionPool
from backend.tools.error_dict_factory import error_output_with_message
from backend.tools.models import CallOutput

# Type alias for tool functions
tool_fn = Callable[[AppRequestArgsBaseModel, DatabaseConnection], CallOutput]

# Mapping of tool names to functions and argument types
TOOL_FUNCS: Dict[str, Tuple[tool_fn, Type[AppRequestArgsBaseModel]]] = {
    "get_stores": (get_stores, AppRequestArgsBaseModel),
    "get_store_by_id": (get_store_by_id, IDArgs),
    "get_coupon_for_store": (get_coupon_for_store, IDArgs),
    "search_product": (search_product, ProductRequestArts),
    "get_products_by_store": (get_products_by_store, IDArgs),
    "get_coupon_for_product": (get_coupon_for_product, IDArgs),
    "set_navigation_for_store": (set_navigation_for_store, IDArgs)
}


class ToolManager:
    """
    Tool manager that handles the tools mapping to actual functions.
    """

    def __init__(self, db_pool: ConnectionPool):
        """
        Initialize the tool manager with the given database connection pool.

        :param db_pool: The database connection pool to use.
        """
        self.db_pool = db_pool

    def call_tool(self, name: str, args_json: str) -> Dict[str, Any]:
        """
        Call the tool with the given name and arguments.

        :param name: The name of the tool to call.
        :param args_json: The arguments to pass to the tool.
        :return: The result of the tool call.
        """
        if name not in TOOL_FUNCS:
            return asdict(error_output_with_message(f"Tool not found: {name}"))
        try:
            args = TOOL_FUNCS[name][1](**json.loads(args_json)) if args_json else {}
        except json.JSONDecodeError:
            return asdict(error_output_with_message("Invalid JSON arguments"))
        print(args)
        print(name)
        with self.db_pool.connection() as conn:
            return asdict(TOOL_FUNCS[name][0](args, conn))
