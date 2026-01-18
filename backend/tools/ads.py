from backend.db.db_models import AllStoreAdEntry, DefaultAdEntry, AdByStoreEntry
from backend.tools.schemas import AppRequestArgsBaseModel, IDArgs
from backend.db.database_connection import DatabaseConnection
from backend.tools.models import CallOutput
from backend.tools.error_dict_factory import *
from db.queries import GET_ALL_ADS, GET_DEFAULT_AD_BY_STORE, GET_BEST_AD_BY_STORE, GET_COUPON_YES_AD_BY_STORE


def get_all_ads(_: AppRequestArgsBaseModel,
               conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    rows = cursor.execute(GET_ALL_ADS).fetchall()
    if len(rows) == 0:
        return error_output_with_message("No ads found.")
    return CallOutput("success", {"ads": [AllStoreAdEntry(**r).model_dump() for r in rows]})


def get_default_ad_for_store(request_args: IDArgs, conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    row = cursor.execute(GET_DEFAULT_AD_BY_STORE, (request_args.id,)).fetchone()
    if not row:
        return error_output_with_message("No matching store found.")
    return CallOutput("success", {"store": DefaultAdEntry(**row).model_dump()})


def get_ad_coupon(request_args: IDArgs, conn: DatabaseConnection) -> CallOutput:
    cursor = conn.cursor()
    row = cursor.execute(GET_COUPON_YES_AD_BY_STORE, (request_args.id,)).fetchone()
    if not row:
        return error_output_with_message("No matching coupon found.")
    return CallOutput("success", {"coupon": DefaultAdEntry(**row).model_dump()})
