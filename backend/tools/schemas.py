"""
This module exposes the argument schemas for the tool calls as pydantic models.
"""
from pydantic import BaseModel, Field
from typing import Optional


class AppRequestArgsBaseModel(BaseModel):
    """
    App-wide base model, used for encapsulation.
    """
    ...


class ProductRequestArts(AppRequestArgsBaseModel):
    query: str = Field(..., description="The product, category or store name to search for")
    limit: int = Field(default=10, ge=1, le=50, description="Max results to return")


class IDArgs(AppRequestArgsBaseModel):
    id: int = Field(..., description="The unique ID to search for.")

