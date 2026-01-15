PRAGMA foreign_keys = ON;

-- STORES
CREATE TABLE IF NOT EXISTS stores (
  store_id      INTEGER PRIMARY KEY,
  store_name    TEXT NOT NULL UNIQUE
);

-- NAVIGATION ASSETS (per store)
CREATE TABLE IF NOT EXISTS store_navigation (
  store_id       INTEGER PRIMARY KEY,
  map_target_id  TEXT NOT NULL,
  route_path_d   TEXT NOT NULL,

  FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE CASCADE
);

-- PRODUCTS (dry data only)
CREATE TABLE IF NOT EXISTS products (
  product_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  product_name   TEXT NOT NULL,
  category       TEXT NOT NULL,
  store_id       INTEGER NOT NULL,

  FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE CASCADE
);

-- COUPONS (coupon_code generated from rule: normalized UPPER(store_name) + store_id)
CREATE TABLE IF NOT EXISTS coupons (
  store_id     INTEGER PRIMARY KEY,
  coupon_code  TEXT NOT NULL UNIQUE,

  FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ads (
  ad_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  store_id   INTEGER NOT NULL,
  ad_type    TEXT    NOT NULL CHECK (ad_type IN ('image', 'navigation')),
  asset_url  TEXT    NOT NULL,
  trigger    TEXT    NOT NULL CHECK (trigger IN ('default', 'coupon_yes')),
  is_active  INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
  created_at TEXT    NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (store_id) REFERENCES stores(store_id)
);

-- Helpful indices
CREATE INDEX IF NOT EXISTS idx_products_name ON products(product_name);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_store ON products(store_id);
CREATE INDEX IF NOT EXISTS idx_ads_store_trigger_active ON ads (store_id, trigger, is_active);
CREATE INDEX IF NOT EXISTS idx_ads_store_type_active ON ads (store_id, ad_type, is_active);