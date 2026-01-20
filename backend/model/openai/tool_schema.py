"""
This module exposes the tools schema for the OpenAI model call.
"""

# List of tools available to the model in the schema form expected by OpenAI
OPEN_AI_TOOL_SCHEMA = [
    {
        "type": "function",
        "name": "search_product",
        "description": "Returns details about the searched product (or category of products) like name and what stores offer it.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
            },
            "required": ["query"],
            "additionalProperties": False,
        }
    },
    {
        "type": "function",
        "name": "get_products_by_store",
        "description": "Returns a list of all products in a given store.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "int"},
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_coupon_for_product",
        "description": "Returns the coupon associated with the given product.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "int"},
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_stores",
        "description": "List all stores in the mall.",
        "parameters": {
            "type": "object",
            "properties": {
            },

            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_store_by_id",
        "description": "Returns the store with the given id.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "int"},
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_coupon_for_store",
        "description": "Returns the coupon associated with the given store id.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "int"},
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "set_navigation_for_store",
        "description": "Shows the user a map with directions to the store with the given ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "int"},
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    },

]
