# List all stores (used to render clickable store buttons)
GET_STORES = """
SELECT store_id, store_name
FROM stores
ORDER BY store_id ASC;
"""

# Fetch a single store by its ID (basic validation / lookup)
GET_STORE_BY_ID = """
SELECT store_id, store_name
FROM stores
WHERE store_id = ?;
"""

GET_ALL_PRODUCTS = """
SELECT
  p.product_id,
  p.product_name,
  p.category,
  s.store_id,
  s.store_name
  
FROM products p
JOIN stores s ON s.store_id = p.store_id
"""

# Search products by free text:
#    - product name
#    - category
#    - store name
# Returns product info + store info so the UI can show store buttons/results
SEARCH_PRODUCTS = """
SELECT
  p.product_id,
  p.product_name,
  p.category,
  s.store_id,
  s.store_name
FROM products p
JOIN stores s ON s.store_id = p.store_id
WHERE
  LOWER(p.product_name) LIKE LOWER(?) OR
  LOWER(p.category) LIKE LOWER(?) OR
  LOWER(s.store_name) LIKE LOWER(?)
ORDER BY s.store_id, p.product_name
LIMIT ?;
"""

# Get all products for a specific store (optional helper endpoint)
GET_PRODUCTS_BY_STORE = """
SELECT
  product_id, product_name, category
FROM products
WHERE store_id = ?
ORDER BY product_name ASC;
"""

# Get navigation assets for a store:
GET_NAVIGATION_ASSET_BY_STORE = """
SELECT
  s.store_id,
  s.store_name,
  n.map_target_id,
  n.route_path_d
FROM stores s
JOIN store_navigation n ON n.store_id = s.store_id
WHERE s.store_id = ?;
"""

CHECK_DB_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='products';"

# Get coupon by store ID
GET_COUPON_BY_STORE = """
SELECT store_id, coupon_code
FROM coupons
WHERE store_id = ?;
"""

# Get coupon by product ID (because the flow is: product -> store -> coupon)
GET_COUPON_BY_PRODUCT = """
SELECT c.store_id, c.coupon_code
FROM products p
JOIN coupons c ON c.store_id = p.store_id
WHERE p.product_id = ?;
"""

# List all ads (debug / verify data)
GET_ALL_ADS = """
SELECT
  ad_id,
  store_id,
  ad_type,
  asset_url,
  logo_url,
  category,
  is_active,
  created_at
FROM ads
ORDER BY ad_id DESC;
"""

# Get DEFAULT ad for a store (when user selects a store)
GET_DEFAULT_AD_BY_STORE = """
SELECT ad_id, ad_type, asset_url
FROM ads
WHERE store_id = ?
  AND category = 'default'
  AND is_active = 1
ORDER BY ad_id DESC
LIMIT 1;
"""

# Get COUPON-YES ad for a store (when user clicks "Yes" to coupon)
GET_COUPON_YES_AD_BY_STORE = """
SELECT ad_id, ad_type, asset_url
FROM ads
WHERE store_id = ?
  AND category = 'coupon_yes'
  AND is_active = 1
ORDER BY ad_id DESC
LIMIT 1;
"""

# Get best ad for a store (prefer coupon_yes, fallback to default)
# Use this as your main query so the app never breaks if coupon_yes is missing.
GET_BEST_AD_BY_STORE = """
SELECT ad_id, ad_type, asset_url, category
FROM ads
WHERE store_id = ?
  AND is_active = 1
ORDER BY CASE category
  WHEN 'coupon_yes' THEN 0
  ELSE 1
END,
ad_id DESC
LIMIT 1;
"""

# Disable an ad (soft delete)
DISABLE_AD_BY_ID = """
UPDATE ads
SET is_active = 0
WHERE ad_id = ?;
"""

# Delete an ad (hard delete – optional)
DELETE_AD_BY_ID = """
DELETE FROM ads
WHERE ad_id = ?;
"""

GET_NAVIGATION_ASSETS = """
SELECT store_id, map_target_id, route_path_d
FROM store_navigation
"""