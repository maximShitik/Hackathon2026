from backend.server.ad_provider import AdProvider
import time

class NovisignProvider:
    def __init__(self, ad_provider: AdProvider, qr_asset_url, navigation_assets,
                 navigation_timeout_s=10):
        self.ad_provider = ad_provider
        self._pending_nav_call = None
        self._last_navigation_call = 0
        self.qr_asset = qr_asset_url
        self.navigation_assets = navigation_assets
        self.navigation_timeout = navigation_timeout_s

    def get_data(self):
        if self._pending_nav_call is not None:
            self._last_navigation_call = time.time()
            call = self._pending_nav_call
            self._pending_nav_call = None
            return call
        ad = self.ad_provider.get_ad()
        if time.time() - self._last_navigation_call > self.navigation_timeout:
            ad["store"]["uppertext"] = "סרקו את הברקוד ותוכלו לקבל קופון הנחה!"
            ad["store"]["mapurl"] = self.qr_asset
        return ad

    def force_next_ad(self, product):
        self.ad_provider.force_next_ad(product)

    def set_data_for_navigation_asset(self, store_id):
        ad = self.ad_provider.get_ad()
        nav_asset = self.navigation_assets[store_id]
        ad["store"]["uppertext"] = ""
        ad["store"]["mapurl"] = nav_asset
        self._pending_nav_call = ad



