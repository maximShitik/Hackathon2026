PRAGMA foreign_keys = ON;

-- STORES
INSERT INTO stores (store_id, store_name) VALUES
  (1, 'סופר פארם'),
  (2, 'ארומה'),
  (3, 'טבע נאות'),
  (4, 'אופטיקנה');

-- STORE NAVIGATION (placeholders for now)
INSERT INTO store_navigation (store_id, map_target_id, route_image) VALUES
  (1, 'superpharm', 'route_superpharm.png'),
  (2, 'aroma',      'route_aroma.png'),
  (3, 'teva_naot',  'route_teva_naot.png'),
  (4, 'opticana',   'route_opticana.png');

-- COUPONS (rule: STORENAME_IN_UPPERCASE + store_id)
INSERT INTO coupons (store_id, coupon_code) VALUES
  (1, 'SUPERPHARM1'),
  (2, 'AROMA2'),
  (3, 'TEVANAOT3'),
  (4, 'OPTICANA4');

-- PRODUCTS
-- 1) סופר פארם
INSERT INTO products (product_name, category, store_id) VALUES
  ('אקומול', 'בריאות', 1),
  ('נורופן', 'בריאות', 1),
  ('נוטרילון', 'מזון תינוקות', 1),
  ('ACUVUE', 'אופטיקה- עדשות מגע', 1),
  ('Ray-ban', 'אופטיקה- משקפי שמש', 1);

-- 2) ארומה
INSERT INTO products (product_name, category, store_id) VALUES
  ('אספרסו', 'משקאות חמים - קפה', 2),
  ('דניס קינמון', 'מאפים', 2),
  ('בורקס גבינה', 'מאפים', 2),
  ('שקשוקה', 'ארוחות בוקר', 2),
  ('לימונדה', 'משקאות קרים', 2);

-- 3) טבע נאות
INSERT INTO products (product_name, category, store_id) VALUES
  ('נעלי בית', 'הנעלה', 3),
  ('סנדלים', 'הנעלה', 3),
  ('נעלי הליכה', 'הנעלה', 3),
  ('נעלי ריצה', 'הנעלה', 3),
  ('סניקרס', 'הנעלה', 3);

-- 4) אופטיקנה
INSERT INTO products (product_name, category, store_id) VALUES
  ('עדשות מגע יומיות', 'אופטיקה', 4),
  ('עדשות מגע חודשיות', 'אופטיקה', 4),
  ('משקפי ראייה', 'אופטיקה', 4),
  ('משקפי שמש', 'אופטיקה', 4),
  ('נוזל לשימור עדשות מגע', 'אופטיקה', 4);
