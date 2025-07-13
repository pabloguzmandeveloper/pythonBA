# This is a great mini application simulates a market with products and prices.
# The user can add products and prices to the market.
# The user can also see the products registered in the market.
# The user can also update the data of products, whit the product´s id.
# The user can also delete a product, whit the product´s id.
# The user can also searching products by product´s id, optional by name or category.
# The user can also report of the products with some value especified for
# the user, with count equal or greater than limit.

import sqlite3


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


def fields_validator(field, type):
    # Especific validators
    def validate_required_text(value):
        if not value or not value.strip():
            field_names = {
                "name": "nombre del producto",
                "stock": "stock del producto",
                "price": "precio del producto",
            }
            field_name = field_names.get(type, "campo")
            return False, f"El {field_name} es requerido"
        return True, None

    def validate_optional_text(value):
        return True, None  # Siempre válido

    def validate_integer(value):
        if not value or not value.strip():
            return False, "El stock es requerido"
        try:
            int_value = int(value)
            if int_value < 0:
                return False, "El stock debe ser mayor o igual a 0"
            return True, None
        except ValueError:
            return False, "El stock debe ser un número entero válido"

    def validate_float(value):
        if not value or not value.strip():
            return False, "El precio es requerido"
        try:
            float_value = float(value)
            if float_value < 0:
                return False, "El precio debe ser mayor o igual a 0"
            return True, None
        except ValueError:
            return False, "El precio debe ser un número decimal válido"

    # Validators dictionary (mapa como en TypeScript)
    validators = {
        "name": validate_required_text,
        "description": validate_optional_text,
        "stock": validate_integer,
        "price": validate_float,
        "category": validate_optional_text,
    }

    # Validar que el tipo de campo existe
    if type not in validators:
        return False, f"Tipo de campo '{type}' no válido"

    # Ejecutar la validación correspondiente
    return validators[type](field)


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

    for field_value, field_type in fields_to_validate:
        is_valid, error_message = fields_validator(field_value, field_type)
        if not is_valid:
            print(f"Error en {field_type}: {error_message}")
            return

    connection, cursor = open_db()

    cursor.execute(
        """
        INSERT INTO products (name, description, stock, price, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, description, stock, price, category),
    )

    connection.commit()
    print("Product added successfully!!!")
    connection.close()


# Descomentar la siguiente línea para probar la función
# add_product()
