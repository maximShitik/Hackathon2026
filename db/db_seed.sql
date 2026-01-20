PRAGMA foreign_keys = ON;

-- STORES
INSERT INTO stores (store_id, store_name) VALUES
  (1, 'סופר פארם'),
  (2, 'ארומה'),
  (3, 'טבע נאות'),
  (4, 'אופטיקנה');

INSERT INTO store_navigation (store_id, map_target_id, route_path_d) VALUES
  (1, 'superpharm', 'https://hackathon-2026.onrender.com/assets/nav/Super_pharm.png'),
  (2, 'aroma',      'https://hackathon-2026.onrender.com/assets/nav/Aroma.png'),
  (3, 'teva_naot',  'https://hackathon-2026.onrender.com/assets/nav/Teva_naot.png'),
  (4, 'opticana',   'https://hackathon-2026.onrender.com/assets/nav/Opticana.png');


-- COUPONS (rule: STORENAME_IN_UPPERCASE + store_id)
INSERT INTO coupons (store_id, coupon_code) VALUES
  (1, 'SUPERPHARM1'),
  (2, 'AROMA2'),
  (3, 'TEVANAOT3'),
  (4, 'OPTICANA4');

-- PRODUCTS
-- 1) סופר פארם
INSERT INTO products (product_name, category, store_id) VALUES
  ('אקומול', 'תרופות', 1),
  ('נורופן', 'תרופות', 1),
  ('נוטרילון', 'מזון תינוקות', 1),
  ('ACUVUE', 'אופטיקה', 1),
  ('Ray-ban', 'אופטיקה', 1);

-- 2) ארומה
INSERT INTO products (product_name, category, store_id) VALUES
  ('אספרסו', 'משקאות', 2),
  ('דניס קינמון', 'אוכל', 2),
  ('בורקס גבינה', 'אוכל', 2),
  ('שקשוקה', 'אוכל', 2),
  ('לימונדה', 'משקאות', 2);

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


INSERT INTO ads (store_id, ad_type, asset_url, logo_url, category) VALUES
(1, 'image', 'https://hackathon-2026.onrender.com/assets/assets/super_pharm.jpg', 'https://hackathon-2026.onrender.com/assets/super_logo.jpg', 'default'),
(1, 'image', 'https://hackathon-2026.onrender.com/assets/assets/gl.jpg', 'https://hackathon-2026.onrender.com/assets/super_logo.jpg', 'אופטיקה'),
(2, 'image', 'https://hackathon-2026.onrender.com/assets/assets/moka.png', 'https://hackathon-2026.onrender.com/assets/aroma_logo.png', 'default'),
(2, 'image', 'https://hackathon-2026.onrender.com/assets/assets/shakshu.png', 'https://hackathon-2026.onrender.com/assets/aroma_logo.png', 'אוכל'),
(3, 'image', 'https://hackathon-2026.onrender.com/assets/assets/tev_asset.jpg', 'https://hackathon-2026.onrender.com/assets/teva_naot_logo.png', 'default'),
(4, 'image', 'https://hackathon-2026.onrender.com/assets/assets/optic.png', 'https://hackathon-2026.onrender.com/assets/optic_logo.jpg', 'default'),
(4, 'image', 'https://hackathon-2026.onrender.com/assets/assets/gl.jpg', 'https://hackathon-2026.onrender.com/assets/optic_logo.jpg', 'אופטיקה');