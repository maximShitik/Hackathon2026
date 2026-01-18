"""
This module exposes the database entries as pydantic models.
"""
from pydantic import BaseModel, ConfigDict
from typing import List


class StoreEntry(BaseModel):
    """
    Store model.
    """
    model_config = ConfigDict(from_attributes=True)
    store_id: int
    store_name: str


class ProductEntry(BaseModel):
    """
    Product model.
    """
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    product_name: str
    category: str
    store_id: int
    store_name: str


class StoreInventoryEntry(BaseModel):
    """
    Store inventory model, by products.
    """
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    product_name: str
    category: str


class NavigationEntry(BaseModel):
    """
    Navigation model.
    """
    model_config = ConfigDict(from_attributes=True)
    store_id: int
    store_name: str
    map_target_id: str
    route_path_d: str


class CouponEntry(BaseModel):
    """
    Coupon model.
    """
    model_config = ConfigDict(from_attributes=True)
    store_id: int
    coupon_code: str


class AllStoreAdEntry(BaseModel):
    """
    All Ads of a store model.
    """
    model_config = ConfigDict(from_attributes=True)
    ad_id: int
    store_id: int
    ad_type: str
    asset_url: str
    trigger: str
    is_active: bool
    created_at: str


class DefaultAdEntry(BaseModel):
    """
    Default ad model.
    """
    model_config = ConfigDict(from_attributes=True)
    ad_id: int
    ad_type: str
    asset_url: str


class AdByStoreEntry(BaseModel):
    """
    Ad by store model.
    """
    model_config = ConfigDict(from_attributes=True)
    ad_id: int
    ad_type: str
    asset_url: str
    trigger: str
