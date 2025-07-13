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


def add_product():
    name = input("Enter the product name: ")
    description = input("Enter the product description: ")
    stock = input("Enter the product stock: ")
    price = input("Enter the product price: ")
    category = input("Enter the product category: ")

    # Validaciones usando la función centralizada
    fields_to_validate = [
        (name, "name"),
        (description, "description"),
        (stock, "stock"),
        (price, "price"),
        (category, "category"),
    ]
    # Dictionary for processed fields
    processed_fields = {}

    for field_value, field_type in fields_to_validate:
        is_valid, error_message, processed_value = fields_validator(
            field_value, field_type
        )
        if not is_valid:
            print(error_message)
            return
        processed_fields[field_type] = processed_value  # Save processed value

    connection, cursor = open_db()

    cursor.execute(
        """
        INSERT INTO products (name, description, stock, price, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            processed_fields["name"],
            processed_fields["description"],
            processed_fields["stock"],
            processed_fields["price"],
            processed_fields["category"],
        ),  # Use processed values
    )

    connection.commit()
    print("Product added successfully!!!")
    connection.close()


# Descomentar la siguiente línea para probar la función
add_product()
