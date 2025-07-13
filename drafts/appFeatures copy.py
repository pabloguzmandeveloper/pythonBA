"""
App Features - Database operations and CRUD functions
"""

import sqlite3


def setup_database():
    """Initialize the database and create tables if they don't exist"""
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            stock INTEGER NOT NULL,
            price REAL NOT NULL,
            category TEXT
        )
        """
    )
    connection.commit()
    return connection


def get_database_connection():
    """Get a database connection"""
    return sqlite3.connect("inventory.db")


def add_product_to_db(name, description, stock, price, category):
    """Add a new product to the database"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products (name, description, stock, price, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, description, stock, price, category),
    )
    connection.commit()
    product_id = cursor.lastrowid
    connection.close()
    return product_id


def get_all_products():
    """Get all products from the database"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products ORDER BY id")
    products = cursor.fetchall()
    connection.close()
    return products


def search_product_by_id(product_id):
    """Search for a product by ID"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    connection.close()
    return product


def search_products_by_name(name):
    """Search for products by name (partial match)"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{name}%",))
    products = cursor.fetchall()
    connection.close()
    return products


def search_products_by_category(category):
    """Search for products by category"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products WHERE category LIKE ?", (f"%{category}%",))
    products = cursor.fetchall()
    connection.close()
    return products


def update_product_in_db(product_id, name, description, stock, price, category):
    """Update an existing product in the database"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE products 
        SET name = ?, description = ?, stock = ?, price = ?, category = ?
        WHERE id = ?
        """,
        (name, description, stock, price, category, product_id),
    )
    connection.commit()
    rows_affected = cursor.rowcount
    connection.close()
    return rows_affected > 0


def delete_product_from_db(product_id):
    """Delete a product from the database"""
    connection = get_database_connection()
    cursor = connection.cursor()

    # First get the product name for confirmation
    cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if product:
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        connection.commit()
        rows_affected = cursor.rowcount
        connection.close()
        return product[0], rows_affected > 0
    else:
        connection.close()
        return None, False


def get_products_count():
    """Get total number of products"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    connection.close()
    return count


def get_inventory_value():
    """Calculate total inventory value"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT SUM(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL) * stock) FROM products"
    )
    total_value = cursor.fetchone()[0] or 0
    connection.close()
    return total_value


def get_low_stock_count(threshold=10):
    """Get count of products with low stock"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM products WHERE CAST(stock AS INTEGER) < ?", (threshold,)
    )
    count = cursor.fetchone()[0]
    connection.close()
    return count


def get_products_by_category():
    """Get products grouped by category"""
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT category, COUNT(*) FROM products GROUP BY category")
    categories = cursor.fetchall()
    connection.close()
    return categories
