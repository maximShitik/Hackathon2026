import random
from abc import ABC, abstractmethod
import numpy as np
from backend.db.database_connection import DatabaseConnection
from backend.tools.products import get_all_products
from backend.tools.ads import get_all_ads


class AdProvider(ABC):

    @abstractmethod
    def get_ad(self):
        ...

    @abstractmethod
    def force_next_ad(self, product):
        ...


class MockAdProvider(AdProvider):
    def __init__(self, conn: DatabaseConnection, window_size=5):
        products = get_all_products(None, conn=conn)
        assert window_size <= len(products), "Not enough products for the window size."
        ads = get_all_ads(None, conn).data["ads"]
        self.ads = self.build_ads(ads, products)
        self.products = products
        self.window_size = window_size
        self.probs = np.random.dirichlet(np.ones(len(products)), size=1)[0]
        self.cur_selection = np.random.choice(self.ads, size=window_size, replace=False,
                                              p=self.probs)
        self.next_ad = 0
        self.forced_ad = None

    def get_ad(self):
        if self.forced_ad is not None:
            product = self.forced_ad
            self.forced_ad = None
            return product
        product = self.cur_selection[self.next_ad]
        self.next_ad += 1
        if self.next_ad == self.window_size:
            self.cur_selection = np.random.choice(self.ads, size=self.window_size,
                                                  replace=False, p=self.probs)
            self.next_ad = 0
        return product

    def force_next_ad(self, product):
        for ad in self.ads:
            if ad["product_name"] == product["product_name"]:
                self.forced_ad = ad
                return

    def build_ads(self, ads, products):
        new_ads = []
        for p in products:
            data = {
                "store": {
                    'product_name': p["product_name"]
                }
            }
            found_cat = False
            for ad in ads:
                if p["store_id"] == ad["store_id"]:
                    data["store"]["logourl"] = ad["logo_url"]
                    if p['category'] == ad['category']:
                        found_cat = True
                        data["store"]["asseturl"] = ad["asset_url"]
                    if not found_cat:
                        data["store"]["asseturl"] = ad["asset_url"]
            new_ads.append(data)
        return new_ads





