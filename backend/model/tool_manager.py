"""
This module exposes the tool manager, alongisde the tools mapping to actual functions.

Classes:
    ToolManager: Class that handles tools mapping to actual functions and calling them.
"""
import json
from typing import Any, Callable, Dict, Tuple, Type, Union
from dataclasses import asdict

from backend.tools.schemas import *
from backend.tools.medication import get_medication_by_name, find_medications_by_ingredient
from backend.tools.inventory import check_inventory, list_locations
from backend.tools.ticket import create_support_ticket, get_ticket
from backend.tools.reserve_prescription import request_reservation, get_reservation
from backend.db.database_connection import DatabaseConnection
from backend.db.connection_pool import ConnectionPool
from backend.tools.error_dict_factory import error_output_with_message
from backend.tools.models import CallOutput

# Type alias for tool functions
tool_fn = Callable[[AppRequestArgsBaseModel, DatabaseConnection], CallOutput]

# Mapping of tool names to functions and argument types
TOOL_FUNCS: Dict[str, Tuple[tool_fn, Type[AppRequestArgsBaseModel]]] = {
    "get_medication_by_name": (get_medication_by_name, MedicationSearchArgs),
    "find_medications_by_ingredient": (find_medications_by_ingredient, IngredientSearchArgs),
    "check_inventory": (check_inventory, InventoryRequest),
    "list_locations": (list_locations, ListLocationsRequest),
    "create_support_ticket": (create_support_ticket, TicketRequest),
    "get_ticket": (get_ticket, GetByIDRequest),
    "request_reservation": (request_reservation, ReservationRequestArgs),
    "get_reservation": (get_reservation, GetByIDRequest)
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
