
DROP DATABASE IF EXISTS grocery_store;
CREATE DATABASE grocery_store;
USE grocery_store;


CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    deleted_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    deleted_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    current_stock INT NOT NULL DEFAULT 0,
    reorder_point INT NOT NULL DEFAULT 10,
    category_id INT,
    supplier_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    deleted_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
);


CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('Cash', 'Card', 'UPI') NOT NULL DEFAULT 'Cash',
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE
);


CREATE TABLE sale_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);


CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_supplier ON products(supplier_id);
CREATE INDEX idx_products_stock ON products(current_stock);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_categories_active ON categories(is_active);
CREATE INDEX idx_suppliers_active ON suppliers(is_active);
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_sale_items_sale ON sale_items(sale_id);
CREATE INDEX idx_sale_items_product ON sale_items(product_id);


CREATE VIEW deleted_products AS SELECT * FROM products WHERE is_active = FALSE;
CREATE VIEW deleted_categories AS SELECT * FROM categories WHERE is_active = FALSE;
CREATE VIEW deleted_suppliers AS SELECT * FROM suppliers WHERE is_active = FALSE;


INSERT INTO admins (username, password, name, email) VALUES 
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrator', 'admin@grocerystore.in');



DELIMITER $$

CREATE TRIGGER trg_update_stock_after_sale
AFTER INSERT ON sale_items
FOR EACH ROW
BEGIN
    UPDATE products
    SET current_stock = current_stock - NEW.quantity
    WHERE id = NEW.product_id;
END $$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE get_monthly_revenue(IN p_year INT, IN p_month INT)
BEGIN
    SELECT 
        IFNULL(SUM(total_amount), 0) AS monthly_revenue
    FROM sales
    WHERE YEAR(sale_date) = p_year
      AND MONTH(sale_date) = p_month;
END $$

DELIMITER ;
