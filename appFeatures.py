# This is a great mini application simulates a market with products and prices.
# The user can add products and prices to the market.
# The user can also see the products registered in the market.
# The user can also update the data of products, whit the product´s id.
# The user can also delete a product, whit the product´s id.
# The user can also searching products by product´s id, optional by name or category.
# The user can also report of the products with some value especified for
# the user, with count equal or greater than limit.

import sqlite3

from validators import fields_validator


def open_db():
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


def add_product():
    print("=== Add New Product ===\n")

    name = get_valid_input("Enter the product name: ", "name")
    description = get_valid_input("Enter the product description: ", "description")
    stock = get_valid_input("Enter the product stock: ", "stock")
    price = get_valid_input("Enter the product price: ", "price")
    category = get_valid_input("Enter the product category: ", "category")

    connection, cursor = open_db()

    cursor.execute(
        """
        INSERT INTO products (name, description, stock, price, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, description, stock, price, category),
    )

    connection.commit()
    print("\n✅ Product added successfully!!!")
    connection.close()


def show_products():
    print("=== Show Products ===\n")

    connection, cursor = open_db()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()


def search_product():
    print("=== Search Product ===\n")

    connection, cursor = open_db()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()


def update_product():
    print("=== Update Product ===\n")

    connection, cursor = open_db()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()


def delete_product():
    print("=== Delete Product ===\n")

    connection, cursor = open_db()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()


def custom_report():
    print("=== Custom Report ===\n")

    connection, cursor = open_db()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
