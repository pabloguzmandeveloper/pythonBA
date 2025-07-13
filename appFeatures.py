"""
App Features - Database operations and CRUD functions
"""

import sqlite3

from validators import fields_validator


def get_database_connection():
    """Get a database connection"""
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

    return connection, cursor


def get_valid_input(prompt, field_type):
    while True:
        user_input = input(prompt)
        is_valid, error_message, processed_value = fields_validator(
            user_input, field_type
        )
        if is_valid:
            return processed_value
        print(f"❌ Error: {error_message}")
        print("Please try again.\n")


def get_product_inputs():
    """Get the 5 standard product inputs with validation"""
    name = get_valid_input("Enter the product name: ", "name")
    description = get_valid_input("Enter the product description: ", "description")
    stock = get_valid_input("Enter the product stock: ", "stock")
    price = get_valid_input("Enter the product price: ", "price")
    category = get_valid_input("Enter the product category: ", "category")
    return name, description, stock, price, category


def add_product():
    """Add a new product to the database"""
    print("=== Add New Product ===\n")

    name, description, stock, price, category = get_product_inputs()

    connection, cursor = get_database_connection()

    """ Add a new product to the database if the input is valid """
    cursor.execute(
        """
        INSERT INTO products (name, description, stock, price, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, description, stock, price, category),
    )

    """ Commit the changes to the database and close the connection """
    connection.commit()
    product_id = cursor.lastrowid
    print("\n✅ Product with ID: ", product_id, "added successfully!!!")
    connection.close()


def get_all_products():
    """Get all products from the database"""
    connection, cursor = get_database_connection()

    cursor.execute("SELECT * FROM products ORDER BY id")
    products = cursor.fetchall()
    connection.close()
    return products


def search_product_by_id(product_id):
    """Search for a product by ID"""
    connection, cursor = get_database_connection()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    connection.close()
    return product


def search_products_by_name(name):
    """Search for products by name (partial match)"""
    connection, cursor = get_database_connection()

    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{name}%",))
    products = cursor.fetchall()
    connection.close()
    return products


def search_products_by_category(category):
    """Search for products by category"""
    connection, cursor = get_database_connection()

    cursor.execute("SELECT * FROM products WHERE category LIKE ?", (f"%{category}%",))
    products = cursor.fetchall()
    connection.close()
    return products


def update_product_in_db(product_id, name, description, stock, price, category):
    """Update an existing product in the database"""
    connection, cursor = get_database_connection()

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


def update_product():
    """Update an existing product with UI"""
    print("=== Update Product ===\n")

    # Get product ID
    product_id = get_valid_input("Enter the product ID to update: ", "id")

    # Get current product data
    current_product = search_product_by_id(product_id)

    if not current_product:
        print("❌ Product not found.")
        return

    # Extract current values
    current_name = current_product[1]
    current_description = current_product[2]
    current_stock = current_product[3]
    current_price = current_product[4]
    current_category = current_product[5]

    print(f"\nUpdating product: {current_name}")
    print("(Press Enter to keep current value)")

    # Get new values with current values as default
    name_input = input(f"Name [{current_name}]: ").strip()
    name = (
        get_valid_input(f"Name [{current_name}]: ", "name")
        if name_input
        else current_name
    )

    desc_input = input(f"Description [{current_description}]: ").strip()
    description = (
        get_valid_input(f"Description [{current_description}]: ", "description")
        if desc_input
        else current_description
    )

    stock_input = input(f"Stock [{current_stock}]: ").strip()
    stock = (
        get_valid_input(f"Stock [{current_stock}]: ", "stock")
        if stock_input
        else current_stock
    )

    price_input = input(f"Price [{current_price}]: ").strip()
    price = (
        get_valid_input(f"Price [{current_price}]: ", "price")
        if price_input
        else current_price
    )

    category_input = input(f"Category [{current_category}]: ").strip()
    category = (
        get_valid_input(f"Category [{current_category}]: ", "category")
        if category_input
        else current_category
    )

    # Update in database
    success = update_product_in_db(
        product_id, name, description, stock, price, category
    )

    if success:
        print("✅ Product updated successfully!")
    else:
        print("❌ Error updating product.")


update_product()


def delete_product_from_db(product_id):
    """Delete a product from the database"""
    connection, cursor = get_database_connection()

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
    connection, cursor = get_database_connection()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    connection.close()
    return count


def get_inventory_value():
    """Calculate total inventory value"""
    connection, cursor = get_database_connection()

    cursor.execute(
        "SELECT SUM(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL) * stock) FROM products"
    )
    total_value = cursor.fetchone()[0] or 0
    connection.close()
    return total_value


def get_low_stock_count(threshold=10):
    """Get count of products with low stock"""
    connection, cursor = get_database_connection()

    cursor.execute(
        "SELECT COUNT(*) FROM products WHERE CAST(stock AS INTEGER) < ?", (threshold,)
    )
    count = cursor.fetchone()[0]
    connection.close()
    return count


def get_products_by_category():
    """Get products grouped by category"""
    connection, cursor = get_database_connection()

    cursor.execute("SELECT category, COUNT(*) FROM products GROUP BY category")
    categories = cursor.fetchall()
    connection.close()
    return categories
