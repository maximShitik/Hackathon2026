import datetime
from typing import Dict, Any
import httpx

from backend.server.ad_provider import AdProvider
import time


async def push_to_novisign_async(data_items: Dict[str, Dict[str, Any]], *,
                                 api_key="reckru_LYMXHua9gz1fwwKoK49hh5Cz5di2rb06ojOTzYs5FvcqT-H0MqVp4W-JL",
                                 studio_domain: str = "app.novisign.com",
                                 items_group="mall-signage", timeout: int = 10) -> Dict[str, Any]:
    url = f"https://{studio_domain}/catalog/items/{items_group}"

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
    }

    payload = {
        "data": data_items
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers,
        )

    if response.status_code >= 400:
        raise RuntimeError(
            f"NoviSign API error {response.status_code}: {response.text}"
        )

    return {
        "success": True,
        "items_updated": len(data_items),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "response": response.json(),
    }



class NovisignProvider:

    def __init__(self, ad_provider: AdProvider, qr_asset_url, navigation_assets,
                 navigation_timeout_s=10):
        self.ad_provider = ad_provider
        self._last_data = None
        self._last_navigation_call = 0
        self.qr_asset = qr_asset_url
        self.navigation_assets = navigation_assets
        self.navigation_timeout = navigation_timeout_s

    def get_data(self):
        ad = self.ad_provider.get_ad()
        if time.time() - self._last_navigation_call > self.navigation_timeout:
            ad["store"]["uppertext"] = "סרקו את הברקוד ותוכלו לקבל קופון הנחה!"
            ad["store"]["mapurl"] = self.qr_asset
        self._last_data = ad
        return ad

    def force_next_ad(self, product):
        self.ad_provider.force_next_ad(product)

    def get_data_for_navigation_asset(self, store_id):
        if self._last_data is None:
            self._last_data = self.ad_provider.get_ad()
        nav_asset = self.navigation_assets[store_id]
        self._last_data["store"]["uppertext"] = ""
        self._last_data["store"]["mapurl"] = nav_asset
        self._last_navigation_call = time.time()
        return self._last_data


