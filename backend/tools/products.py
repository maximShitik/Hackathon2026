from backend.db.db_models import ProductEntry, StoreInventoryEntry, CouponEntry
from backend.tools.schemas import ProductRequestArts, IDArgs
from backend.db.database_connection import DatabaseConnection
from backend.tools.models import CallOutput
from backend.tools.error_dict_factory import *
from db.queries import SEARCH_PRODUCTS, GET_PRODUCTS_BY_STORE, GET_COUPON_BY_PRODUCT


def search_product(request_args: ProductRequestArts,
                   conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    rows = cursor.execute(SEARCH_PRODUCTS, (request_args.query, request_args.query,
                                            request_args.query, request_args.limit)).fetchall()
    if len(rows) == 0:
        return error_output_with_message("No matching products found.")
    return CallOutput("success", {"products": [ProductEntry(**r).model_dump() for r in rows]})


def get_products_by_store(request_args: IDArgs, conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    rows = cursor.execute(GET_PRODUCTS_BY_STORE, (request_args.id,)).fetchall()
    if len(rows) == 0:
        return error_output_with_message("No matching products found.")
    return CallOutput("success", {"products": [StoreInventoryEntry(**r).model_dump() for r in rows]})


def get_coupon_for_product(request_args: IDArgs, conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    rows = cursor.execute(GET_COUPON_BY_PRODUCT, (request_args.id,)).fetchall()
    if len(rows) == 0:
        return error_output_with_message("No matching coupon found.")
    return CallOutput("success", {"coupon": [CouponEntry(**r).model_dump() for r in rows]})
