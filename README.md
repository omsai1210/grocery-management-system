# Grocery Management System

A robust, full-stack Grocery Management System designed to streamline retail operations. This application provides a comprehensive dashboard for administrators to manage inventory, suppliers, sales, and view real-time analytics. Built with Python (Flask) and MySQL.

## 🚀 Key Features

*   **Secure Authentication**: JWT-based admin authentication implementation.
*   **Inventory Management**: Full CRUD operations for Products and Categories.
*   **Stock Control**: Real-time stock tracking with low-stock alerts and automatic deduction upon sale.
*   **Supplier Management**: Database of suppliers linked to products.
*   **Point of Sale (POS)**: Efficient sales processing supporting multi-item orders and payment method tracking.
*   **Analytics Dashboard**: Visual insights into Total Sales, Monthly Revenue, Top Selling Products, and Category performance.
*   **Date/Time Handling**: configured for IST (Indian Standard Time) for accurate local reporting.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **Database**: MySQL
*   **Authentication**: JSON Web Tokens (JWT)
*   **API**: RESTful architecture
*   **Environment**: Dotenv for configuration management

## ⚙️ Installation & Setup

### Prerequisites
*   Python 3.8+
*   MySQL Server

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/grocery-management-system.git
cd grocery-management-system
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
1.  Create a MySQL database (e.g., `grocery_store`).
2.  Import the schema:
    ```bash
    mysql -u root -p grocery_store < schema.sql
    ```
    *(Or use your preferred GUI tool like MySQL Workbench / DBeaver)*

### 5. Environment Variables
Create a `.env` file in the root directory:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=grocery_store
DB_PORT=3306
```

### 6. Run the Application
```bash
python app.py
```
The API will be available at `http://localhost:5000`.

## 📚 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/login` | Admin login to receive JWT |
| `GET` | `/api/admin/products` | List all products |
| `POST` | `/api/admin/sales` | Create a new sale transaction |
| `GET` | `/api/admin/analytics/snapshot` | Get dashboard summary stats |
| ... | ... | ... |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
