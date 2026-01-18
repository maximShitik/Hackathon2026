from backend.db.db_models import StoreEntry, CouponEntry, NavigationEntry
from backend.tools.schemas import AppRequestArgsBaseModel, IDArgs
from backend.db.database_connection import DatabaseConnection
from backend.tools.models import CallOutput
from backend.tools.error_dict_factory import *
from db.queries import GET_STORES, GET_STORE_BY_ID, GET_COUPON_BY_STORE, GET_NAVIGATION_ASSET_BY_STORE


def get_stores(_: AppRequestArgsBaseModel,
               conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    rows = cursor.execute(GET_STORES).fetchall()
    if len(rows) == 0:
        return error_output_with_message("No stores found.")
    return CallOutput("success", {"stores": [StoreEntry(**r).model_dump() for r in rows]})


def get_store_by_id(request_args: IDArgs, conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    row = cursor.execute(GET_STORE_BY_ID, (request_args.id,)).fetchone()
    if not row:
        return error_output_with_message("No matching store found.")
    return CallOutput("success", {"store": StoreEntry(**row).model_dump()})


def get_coupon_for_store(request_args: IDArgs, conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    row = cursor.execute(GET_COUPON_BY_STORE, (request_args.id,)).fetchone()
    if not row:
        return error_output_with_message("No matching coupon found.")
    return CallOutput("success", {"coupon": CouponEntry(**row).model_dump()})


def get_navigation_for_store(request_args: IDArgs, conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    row = cursor.execute(GET_NAVIGATION_ASSET_BY_STORE, (request_args.id,)).fetchone()
    if not row:
        return error_output_with_message("No matching navigation asset found.")
    return CallOutput("success", {"asset": NavigationEntry(**row).model_dump()})