from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from functools import wraps

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'omsai000000',
    'database': 'grocery_store'
}

# Token storage (in production, use Redis or database)
active_tokens = {}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return secrets.token_hex(32)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token not in active_tokens:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

def get_ist_now():
    # IST is UTC + 5:30
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM admins WHERE username = %s', (username,))
    admin = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if admin and admin['password'] == hash_password(password):
        token = generate_token()
        active_tokens[token] = {
            'admin_id': admin['id'],
            'username': admin['username'],
            'expires': datetime.now() + timedelta(hours=8)
        }
        return jsonify({
            'token': token,
            'admin': {
                'id': admin['id'],
                'username': admin['username'],
                'name': admin['name']
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@token_required
def logout():
    token = request.headers.get('Authorization')
    if token in active_tokens:
        del active_tokens[token]
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/admin/categories', methods=['GET'])
@token_required
def get_categories():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM categories WHERE is_active = TRUE ORDER BY name')
    categories = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(categories), 200

@app.route('/api/admin/categories', methods=['POST'])
@token_required
def create_category():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({'error': 'Category name is required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO categories (name, description, is_active) VALUES (%s, %s, TRUE)',
            (name, description)
        )
        conn.commit()
        category_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'id': category_id, 'message': 'Category created'}), 201
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/categories/<int:id>', methods=['PUT'])
@token_required
def update_category(id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({'error': 'Category name is required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE categories SET name = %s, description = %s WHERE id = %s AND is_active = TRUE',
            (name, description, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Category updated'}), 200
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/categories/<int:id>', methods=['DELETE'])
@token_required
def delete_category(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        # Soft delete - mark as inactive instead of deleting
        cursor.execute(
            'UPDATE categories SET is_active = FALSE, deleted_at = NOW() WHERE id = %s',
            (id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Category deleted'}), 200
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products', methods=['GET'])
@token_required
def get_products():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.*, c.name as category_name, s.name as supplier_name 
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id AND c.is_active = TRUE
        LEFT JOIN suppliers s ON p.supplier_id = s.id AND s.is_active = TRUE
        WHERE p.is_active = TRUE
        ORDER BY p.name
    ''')
    products = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(products), 200

@app.route('/api/admin/products/lowstock', methods=['GET'])
@token_required
def get_low_stock_products():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.*, c.name as category_name, s.name as supplier_name 
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id AND c.is_active = TRUE
        LEFT JOIN suppliers s ON p.supplier_id = s.id AND s.is_active = TRUE
        WHERE p.current_stock <= p.reorder_point AND p.is_active = TRUE
        ORDER BY p.current_stock
    ''')
    products = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(products), 200

@app.route('/api/admin/products', methods=['POST'])
@token_required
def create_product():
    data = request.get_json()
    
    required_fields = ['name', 'sku', 'price', 'cost', 'current_stock', 'reorder_point']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO products 
            (name, sku, price, cost, current_stock, reorder_point, category_id, supplier_id, description, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        ''', (
            data['name'], data['sku'], data['price'], data['cost'],
            data['current_stock'], data['reorder_point'],
            data.get('category_id'), data.get('supplier_id'),
            data.get('description', '')
        ))
        conn.commit()
        product_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'id': product_id, 'message': 'Product created'}), 201
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/<int:id>', methods=['PUT'])
@token_required
def update_product(id):
    data = request.get_json()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE products SET 
            name = %s, sku = %s, price = %s, cost = %s,
            current_stock = %s, reorder_point = %s,
            category_id = %s, supplier_id = %s, description = %s
            WHERE id = %s AND is_active = TRUE
        ''', (
            data['name'], data['sku'], data['price'], data['cost'],
            data['current_stock'], data['reorder_point'],
            data.get('category_id'), data.get('supplier_id'),
            data.get('description', ''), id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product updated'}), 200
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        # Soft delete - mark as inactive
        cursor.execute(
            'UPDATE products SET is_active = FALSE, deleted_at = NOW() WHERE id = %s',
            (id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product deleted'}), 200
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/suppliers', methods=['GET'])
@token_required
def get_suppliers():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM suppliers WHERE is_active = TRUE ORDER BY name')
    suppliers = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(suppliers), 200

@app.route('/api/admin/suppliers', methods=['POST'])
@token_required
def create_supplier():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Supplier name is required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO suppliers (name, contact_person, phone, email, address, is_active)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        ''', (
            data['name'], data.get('contact_person', ''),
            data.get('phone', ''), data.get('email', ''),
            data.get('address', '')
        ))
        conn.commit()
        supplier_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'id': supplier_id, 'message': 'Supplier created'}), 201
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/suppliers/<int:id>', methods=['PUT'])
@token_required
def update_supplier(id):
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Supplier name is required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE suppliers SET 
            name = %s, contact_person = %s, phone = %s, email = %s, address = %s
            WHERE id = %s AND is_active = TRUE
        ''', (
            data['name'], data.get('contact_person', ''),
            data.get('phone', ''), data.get('email', ''),
            data.get('address', ''), id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Supplier updated'}), 200
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/suppliers/<int:id>', methods=['DELETE'])
@token_required
def delete_supplier(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        # Soft delete
        cursor.execute(
            'UPDATE suppliers SET is_active = FALSE, deleted_at = NOW() WHERE id = %s',
            (id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Supplier deleted'}), 200
    except Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/sales', methods=['GET'])
@token_required
def get_sales():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT s.*, a.name as admin_name
        FROM sales s
        JOIN admins a ON s.admin_id = a.id
        ORDER BY s.sale_date DESC
    ''')
    sales = cursor.fetchall()
    
    for sale in sales:
        cursor.execute('''
            SELECT si.*, p.name as product_name
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = %s
        ''', (sale['id'],))
        sale['items'] = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(sales), 200

@app.route('/api/admin/sales/<int:id>', methods=['GET'])
@token_required
def get_sale(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT s.*, a.name as admin_name
        FROM sales s
        JOIN admins a ON s.admin_id = a.id
        WHERE s.id = %s
    ''', (id,))
    sale = cursor.fetchone()
    
    if sale:
        cursor.execute('''
            SELECT si.*, p.name as product_name, p.sku
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = %s
        ''', (id,))
        sale['items'] = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(sale), 200

@app.route('/api/admin/sales', methods=['POST'])
@token_required
def create_sale():
    data = request.get_json()
    token = request.headers.get('Authorization')
    admin_id = active_tokens[token]['admin_id']
    
    items = data.get('items', [])
    payment_method = data.get('payment_method', 'Cash')
    
    if not items:
        return jsonify({'error': 'No items in sale'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Calculate total and validate stock
        total_amount = 0
        for item in items:
            cursor.execute('SELECT * FROM products WHERE id = %s AND is_active = TRUE', (item['product_id'],))
            product = cursor.fetchone()
            
            if not product:
                raise Exception(f"Product {item['product_id']} not found or inactive")
            
            if product['current_stock'] < item['quantity']:
                raise Exception(f"Insufficient stock for {product['name']}")
            
            total_amount += product['price'] * item['quantity']
        
        # --- IST MODIFICATION STARTS HERE ---
        # Get current IST time using our helper
        sale_date_ist = get_ist_now()

        # Insert sale with explicit IST timestamp instead of SQL's NOW()
        cursor.execute('''
            INSERT INTO sales (admin_id, total_amount, payment_method, sale_date)
            VALUES (%s, %s, %s, %s)
        ''', (admin_id, total_amount, payment_method, sale_date_ist))
        # --- IST MODIFICATION ENDS HERE ---
        
        sale_id = cursor.lastrowid
        
        # Add sale items and update stock (Keep existing logic)
        for item in items:
            cursor.execute('SELECT * FROM products WHERE id = %s', (item['product_id'],))
            product = cursor.fetchone()
            
            cursor.execute('''
                INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                sale_id, item['product_id'], item['quantity'],
                product['price'], product['price'] * item['quantity']
            ))
            
            cursor.execute('''
                UPDATE products SET current_stock = current_stock - %s
                WHERE id = %s
            ''', (item['quantity'], item['product_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'id': sale_id,
            'total_amount': total_amount,
            'message': 'Sale completed successfully'
        }), 201
        
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/analytics/snapshot', methods=['GET'])
@token_required
def get_snapshot():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT COUNT(*) as total FROM products WHERE is_active = TRUE')
    total_products = cursor.fetchone()['total']
    
    cursor.execute('SELECT SUM(current_stock * price) as value FROM products WHERE is_active = TRUE')
    result = cursor.fetchone()
    total_stock_value = result['value'] if result['value'] else 0
    
    cursor.execute('SELECT COUNT(*) as count FROM products WHERE current_stock <= reorder_point AND is_active = TRUE')
    low_stock_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(total_amount) as revenue FROM sales WHERE MONTH(sale_date) = MONTH(NOW())')
    result = cursor.fetchone()
    monthly_revenue = result['revenue'] if result['revenue'] else 0
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'total_products': total_products,
        'total_stock_value': float(total_stock_value),
        'low_stock_count': low_stock_count,
        'monthly_revenue': float(monthly_revenue)
    }), 200

@app.route('/api/admin/analytics/sales_by_month', methods=['GET'])
@token_required
def sales_by_month():
    conn = get_db_connection()
    
    cursor = conn.cursor(dictionary=True)
    # ADDED: DATE_ADD(..., INTERVAL '05:30' HOUR_MINUTE) to align SQL time with IST
    cursor.execute('''
        SELECT 
            DATE_FORMAT(sale_date, '%Y-%m') as month,
            SUM(total_amount) as total
        FROM sales
        WHERE sale_date >= DATE_SUB(DATE_ADD(NOW(), INTERVAL '05:30' HOUR_MINUTE), INTERVAL 12 MONTH)
        GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
        ORDER BY month
    ''')
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(results), 200

@app.route('/api/admin/analytics/sales_by_category', methods=['GET'])
@token_required
def sales_by_category():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT 
            c.name as category,
            SUM(si.subtotal) as total
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        WHERE c.is_active = TRUE
        GROUP BY c.id, c.name
        ORDER BY total DESC
    ''')
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(results), 200

@app.route('/api/admin/analytics/topsellers', methods=['GET'])
@token_required
def top_sellers():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT 
            p.name,
            p.sku,
            SUM(si.quantity) as total_sold,
            SUM(si.subtotal) as revenue
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        WHERE p.is_active = TRUE
        GROUP BY p.id, p.name, p.sku
        ORDER BY total_sold DESC
        LIMIT 10
    ''')
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)