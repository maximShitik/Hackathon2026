-- 1) List all stores (used to render clickable store buttons)
GET_STORES = """
SELECT store_id, store_name
FROM stores
ORDER BY store_id ASC;
"""

-- 2) Fetch a single store by its ID (basic validation / lookup)
GET_STORE_BY_ID = """
SELECT store_id, store_name
FROM stores
WHERE store_id = ?;
"""

-- 3) Search products by free text:
--    - product name
--    - category
--    - store name
-- Returns product info + store info so the UI can show store buttons/results
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

-- 4) Get all products for a specific store (optional helper endpoint)
GET_PRODUCTS_BY_STORE = """
SELECT
  product_id, product_name, category
FROM products
WHERE store_id = ?
ORDER BY product_name ASC;
"""

-- 5) Get navigation assets for a store:
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


-- 6) Get coupon by store ID
GET_COUPON_BY_STORE = """
SELECT store_id, coupon_code
FROM coupons
WHERE store_id = ?;
"""

-- 7) Get coupon by product ID (because the flow is: product -> store -> coupon)
GET_COUPON_BY_PRODUCT = """
SELECT c.store_id, c.coupon_code
FROM products p
JOIN coupons c ON c.store_id = p.store_id
WHERE p.product_id = ?;
"""
