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

-- Helpful indices
CREATE INDEX IF NOT EXISTS idx_products_name ON products(product_name);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_store ON products(store_id);
