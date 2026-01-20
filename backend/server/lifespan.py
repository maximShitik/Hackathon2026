"""
This module is used to set up the database pool and response provider in the app lifespan.

Functions:
    lifespan: Sets up the database pool and response provider in the app lifespan.
"""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
import httpx
import os
import json
from typing import Dict, Any
# from backend.model.gemini.client import GeminiToolUsageClient, SimpleGeminiResponseProvider
# from backend.model.gemini.summary_format_provider import create_gemini_summary_format
from backend.model.openai.client import OpenAIToolResponseProvider, OpenAISimpleResponseProvider
from backend.model.openai.tool_usage_parser import create_summary_format
from backend.model.openai.chat_utils import count_tokens
from backend.model.tool_manager import ToolManager
from backend.model.chat_manager import ChatManager
from backend.db.database_connection import DatabaseConnection
from backend.db.init_db import init_db_if_needed
from backend.db.sqlite_connection import get_db
from backend.db.single_instance_pool import SingleInstancePool
from backend.model.response_provider import ResponseProvider
from backend.server.ad_provider import MockAdProvider
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.server.novisign_provider import NovisignProvider, push_to_novisign_async
from db.queries import GET_NAVIGATION_ASSETS


def _setup_openai_provider(cfg: Dict[str, str], tool_manager: ToolManager) -> ResponseProvider:
    """
    Sets up the OpenAI provider from the given cfg and tool_manager.

    :param cfg: The cfg to use.
    :param tool_manager: The tool manager to use.
    :return: The OpenAI provider.
    """
    api_key = os.environ["OPENAI_API_KEY"]
    model_name = cfg.get("MODEL_NAME", "gpt-5-nano")
    tool_response_provider = OpenAIToolResponseProvider(tool_manager=tool_manager,
                                                        api_key=api_key, model_name=model_name)
    return tool_response_provider
    # simple_response_provider = OpenAISimpleResponseProvider(api_key, model_name)
    # return ChatManager(tool_response_provider, simple_response_provider, create_summary_format,
    #                    token_counter=count_tokens)


# def _setup_gemini_provider(cfg: Dict[str, str], tool_manager: ToolManager) -> ResponseProvider:
#     api_key = cfg["GEMINI_KEY"]
#     model_name = cfg.get("GEMINI_MODEL", "gemini-2.0-flash")
#     tool_response_provider = GeminiToolUsageClient(tool_manager=tool_manager, api_key=api_key,
#                                                    model_name=model_name)
#     simple_response_provider = SimpleGeminiResponseProvider(api_key, model_name)
#     return ChatManager(tool_response_provider, simple_response_provider,
#                        create_gemini_summary_format,
#                        token_counter=None)


def _setup_response_provider(tool_manager: ToolManager) -> ResponseProvider:
    """
    Sets up the response provider from the cfg.json file and the given ToolManager.

    :param tool_manager: The tool manager to use.
    :return: The response provider.
    """
    cfg_path = "cfg.json"  # Path from root folder.
    if not os.path.exists(cfg_path):
        raise RuntimeError(r"To prevent the API key leaking, the CFG file was not added to this "
                           r"repository. In order to run this server, find this function "
                           r"'setup_response_provider' in the file backend\server\main.py and "
                           r"hard code the api_key in the respective variable. Alternatively, "
                           r"create a cfg.json file with the field 'OPENAI_API_KEY' containing "
                           r"the key for open AI usage, or 'GEMINI_KEY' for gemini usage..")
    with open(cfg_path) as f:
        cfg = json.load(f)
    cfg["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
    setup_method = _setup_openai_provider
    return setup_method(cfg, tool_manager)


def _setup_novisign_provider(conn: DatabaseConnection):
    ad_provider = MockAdProvider(conn)
    cursor = conn.cursor()
    rows = cursor.execute(GET_NAVIGATION_ASSETS).fetchall()
    assets = {r["store_id"]: r["route_path_d"] for r in rows}
    qr = "qr-code.png"
    return NovisignProvider(ad_provider, qr, assets)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Sets up the database pool and response provider in the app lifespan.
    """
    cfg_path = "cfg.json"
    with open(cfg_path) as f:
        app.state.use_openAI = json.load(f).get("USE_OPENAI", False)
    app.state.db_pool = SingleInstancePool(get_db)
    init_db_if_needed(app.state.db_pool.get_connection)
    app.state.novisign_provider = _setup_novisign_provider(app.state.db_pool.get_connection())
    app.state.response_provider = _setup_response_provider(ToolManager(app.state.db_pool))
    scheduler = AsyncIOScheduler()

    async def scheduled_update():
        data = app.state.novisign_provider.get_data()
        await push_to_novisign_async(data_items=data)

    scheduler.add_job(scheduled_update, trigger="interval", seconds=10, max_instances=1,
                      coalesce=True)
    scheduler.start()
    app.state.messages = []
    yield
    app.state.db_pool.close()
    scheduler.shutdown()
