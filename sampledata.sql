INSERT INTO categories (id, name, description) VALUES
(1, 'Dairy & Breakfast', 'Milk, eggs, bread, butter, and daily essentials'),
(2, 'Fresh Produce', 'Organic fruits, vegetables, and herbs'),
(3, 'Beverages', 'Soft drinks, juices, water, tea, and coffee'),
(4, 'Snacks & Confectionery', 'Chips, biscuits, chocolates, and namkeen'),
(5, 'Household Essentials', 'Cleaning supplies, paper goods, and hygiene products');

INSERT INTO suppliers (id, name, contact_person, phone, email, address) VALUES
(1, 'FreshFarm Distributors', 'Ramesh Kumar', '9876543210', 'orders@freshfarm.com', '12 Mandi Road, Pune'),
(2, 'Global FMCG Supplies', 'Anita Desai', '9988776655', 'sales@globalfmcg.in', '45 Industrial Area, Mumbai'),
(3, 'PureDairy Co.', 'Suresh Patil', '9123456789', 'suresh@puredairy.com', '88 Milk Colony, Nashik'),
(4, 'Sunrise Beverages', 'Vikram Singh', '9000011111', 'contact@sunrisebev.com', '102 MIDC, Nagpur'),
(5, 'HomeClean Solutions', 'Priya Menon', '8888899999', 'support@homeclean.com', '56 Tech Park, Pune');

INSERT INTO products (id, name, sku, price, cost, current_stock, reorder_point, category_id, supplier_id) VALUES
(1, 'Amul Gold Milk (1L)', 'DRY001', 72.00, 68.00, 5, 15, 1, 3),
(2, 'Britannia Whole Wheat Bread', 'DRY002', 45.00, 38.00, 20, 10, 1, 1),
(3, 'Amul Salted Butter (500g)', 'DRY003', 275.00, 250.00, 4, 10, 1, 3),
(4, 'Farm Fresh Eggs (Pack of 6)', 'DRY004', 60.00, 45.00, 50, 10, 1, 1),
(5, 'Washington Apples (1kg)', 'FRT001', 220.00, 160.00, 35, 10, 2, 1),
(6, 'Robusta Bananas (1 Dozen)', 'FRT002', 60.00, 40.00, 8, 12, 2, 1),
(7, 'Fresh Onion (1kg)', 'VEG001', 40.00, 25.00, 100, 20, 2, 1),
(8, 'Organic Potato (1kg)', 'VEG002', 35.00, 20.00, 80, 20, 2, 1),
(9, 'Coca-Cola (750ml)', 'BEV001', 45.00, 35.00, 120, 24, 3, 4),
(10, 'Real Mixed Fruit Juice (1L)', 'BEV002', 110.00, 90.00, 40, 10, 3, 2),
(11, 'Nescafe Classic Coffee (50g)', 'BEV003', 160.00, 130.00, 25, 10, 3, 2),
(12, 'Red Label Tea (500g)', 'BEV004', 280.00, 240.00, 30, 10, 3, 2),
(13, 'Lays Magic Masala (Large)', 'SNK001', 20.00, 15.00, 55, 20, 4, 2),
(14, 'Cadbury Dairy Milk Silk', 'SNK002', 180.00, 150.00, 15, 10, 4, 2),
(15, 'Parle-G Gold Biscuits', 'SNK003', 10.00, 8.00, 200, 50, 4, 2),
(16, 'Haldiram Bhujia Sev (400g)', 'SNK004', 110.00, 90.00, 45, 15, 4, 2),
(17, 'Surf Excel Matic Liquid (1L)', 'HSE001', 230.00, 190.00, 18, 10, 5, 5),
(18, 'Dettol Handwash Refill', 'HSE002', 99.00, 80.00, 2, 10, 5, 5),
(19, 'Vim Dishwash Bar', 'HSE003', 25.00, 18.00, 60, 20, 5, 5),
(20, 'Colin Glass Cleaner', 'HSE004', 105.00, 85.00, 12, 10, 5, 5);

INSERT INTO sales (id, admin_id, total_amount, payment_method, sale_date) VALUES
(1, 1, 335.00, 'Cash', DATE_SUB(NOW(), INTERVAL 95 DAY)),
(2, 1, 45.00, 'UPI', DATE_SUB(NOW(), INTERVAL 92 DAY)),
(3, 1, 550.00, 'Card', DATE_SUB(NOW(), INTERVAL 91 DAY));

INSERT INTO sales (id, admin_id, total_amount, payment_method, sale_date) VALUES
(4, 1, 120.00, 'Cash', DATE_SUB(NOW(), INTERVAL 65 DAY)),
(5, 1, 80.00, 'UPI', DATE_SUB(NOW(), INTERVAL 64 DAY)),
(6, 1, 460.00, 'UPI', DATE_SUB(NOW(), INTERVAL 62 DAY)),
(7, 1, 99.00, 'Cash', DATE_SUB(NOW(), INTERVAL 61 DAY)),
(8, 1, 1000.00, 'Card', DATE_SUB(NOW(), INTERVAL 60 DAY));

INSERT INTO sales (id, admin_id, total_amount, payment_method, sale_date) VALUES
(9, 1, 72.00, 'Cash', DATE_SUB(NOW(), INTERVAL 35 DAY)),
(10, 1, 275.00, 'UPI', DATE_SUB(NOW(), INTERVAL 34 DAY)),
(11, 1, 540.00, 'Card', DATE_SUB(NOW(), INTERVAL 33 DAY)),
(12, 1, 1100.00, 'UPI', DATE_SUB(NOW(), INTERVAL 32 DAY)),
(13, 1, 45.00, 'Cash', DATE_SUB(NOW(), INTERVAL 32 DAY)),
(14, 1, 350.00, 'UPI', DATE_SUB(NOW(), INTERVAL 31 DAY)),
(15, 1, 220.00, 'Cash', DATE_SUB(NOW(), INTERVAL 30 DAY)),
(16, 1, 60.00, 'Cash', DATE_SUB(NOW(), INTERVAL 30 DAY));

INSERT INTO sales (id, admin_id, total_amount, payment_method, sale_date) VALUES
(17, 1, 510.00, 'Card', DATE_SUB(NOW(), INTERVAL 5 DAY)),
(18, 1, 130.00, 'UPI', DATE_SUB(NOW(), INTERVAL 3 DAY)),
(19, 1, 180.00, 'Cash', DATE_SUB(NOW(), INTERVAL 1 DAY)),
(20, 1, 2250.00, 'Card', NOW());

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1, 2, 72.00, 144.00),
(1, 18, 1, 99.00, 99.00),
(1, 9, 2, 45.00, 90.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(2, 2, 1, 45.00, 45.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(3, 3, 2, 275.00, 550.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(4, 6, 2, 60.00, 120.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(5, 7, 2, 40.00, 80.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(6, 17, 2, 230.00, 460.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(7, 18, 1, 99.00, 99.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(8, 12, 2, 280.00, 560.00),
(8, 5, 2, 220.00, 440.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(9, 1, 1, 72.00, 72.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(10, 3, 1, 275.00, 275.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(11, 14, 3, 180.00, 540.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(12, 10, 10, 110.00, 1100.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(13, 9, 1, 45.00, 45.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(14, 20, 2, 105.00, 210.00),
(14, 8, 4, 35.00, 140.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(15, 5, 1, 220.00, 220.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(16, 4, 1, 60.00, 60.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(17, 11, 2, 160.00, 320.00),
(17, 13, 2, 20.00, 40.00),
(17, 15, 15, 10.00, 150.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(18, 13, 2, 20.00, 40.00),
(18, 9, 2, 45.00, 90.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(19, 14, 1, 180.00, 180.00);

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(20, 3, 2, 275.00, 550.00),
(20, 17, 2, 230.00, 460.00),
(20, 5, 2, 220.00, 440.00),
(20, 14, 2, 180.00, 360.00),
(20, 1, 5, 72.00, 360.00),
(20, 7, 2, 40.00, 80.00);