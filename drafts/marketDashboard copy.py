"""
Market Dashboard Application
Advanced product management system with validation
"""

import sqlite3

from validators import fields_validator


class Product:
    def __init__(self, name, description, stock, price, category, product_id=None):
        self.id = product_id
        self.name = name
        self.description = description
        self.stock = stock
        self.price = price
        self.category = category

    def __str__(self):
        return f"ID: {self.id} | {self.name} | {self.price} | Stock: {self.stock} | {self.category}"


class MarketDashboard:
    def __init__(self):
        self.running = True
        self.setup_database()

    def setup_database(self):
        """Initialize the database and create tables if they don't exist"""
        self.connection = sqlite3.connect("inventory.db")
        cursor = self.connection.cursor()

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
        self.connection.commit()

    def show_menu(self):
        """Display the main menu and get user choice"""
        menu = """
        ===== MARKET TECH DASHBOARD =====

        Choose an option to continue:
        1. Add Product
        2. Show All Products
        3. Search Product
        4. Update Product
        5. Delete Product
        6. Generate Report
        7. Exit
        ================================
        """
        print(menu)
        return input("Select an option: ").strip()

    def get_valid_input(self, prompt, field_type):
        """Get valid input from user with real-time validation"""
        while True:
            user_input = input(prompt)
            is_valid, error_message, processed_value = fields_validator(
                user_input, field_type
            )
            if is_valid:
                return processed_value
            print(f"❌ Error: {error_message}")
            print("Please try again.\n")

    def add_product(self):
        """Add a new product with advanced validation"""
        print("\n=== ADD NEW PRODUCT ===\n")

        # Get validated inputs
        name = self.get_valid_input("Enter product name: ", "name")
        description = self.get_valid_input("Enter product description: ", "description")
        stock = self.get_valid_input("Enter product stock: ", "stock")
        price = self.get_valid_input("Enter product price: ", "price")
        category = self.get_valid_input("Enter product category: ", "category")

        # Save to database
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, description, stock, price, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, description, stock, price, category),
        )
        self.connection.commit()

        print(f"\n✅ Product '{name}' added successfully!")
        input("\nPress Enter to continue...")

    def show_all_products(self):
        """Display all products from database"""
        print("\n=== ALL PRODUCTS ===")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products ORDER BY id")
        products = cursor.fetchall()

        if not products:
            print("No products found in the database.")
        else:
            print(
                f"{'ID':<5} {'Name':<20} {'Price':<15} {'Stock':<10} {'Category':<15}"
            )
            print("-" * 70)
            for product in products:
                product_id, name, description, stock, price, category = product
                print(
                    f"{product_id:<5} {name:<20} {price:<15} {stock:<10} {category:<15}"
                )

            print(f"\nTotal products: {len(products)}")

        input("\nPress Enter to continue...")

    def search_product(self):
        """Search products by name, category, or ID"""
        print("\n=== SEARCH PRODUCT ===")
        print("Search options:")
        print("1. By ID")
        print("2. By Name")
        print("3. By Category")

        option = input("\nSelect search option: ").strip()
        cursor = self.connection.cursor()

        if option == "1":
            product_id = input("Enter product ID: ").strip()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        elif option == "2":
            name = input("Enter product name (partial match): ").strip()
            cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{name}%",))
        elif option == "3":
            category = input("Enter category: ").strip()
            cursor.execute(
                "SELECT * FROM products WHERE category LIKE ?", (f"%{category}%",)
            )
        else:
            print("Invalid option.")
            input("\nPress Enter to continue...")
            return

        products = cursor.fetchall()

        if products:
            print(f"\n✅ Found {len(products)} product(s):")
            print(
                f"{'ID':<5} {'Name':<20} {'Price':<15} {'Stock':<10} {'Category':<15}"
            )
            print("-" * 70)
            for product in products:
                product_id, name, description, stock, price, category = product
                print(
                    f"{product_id:<5} {name:<20} {price:<15} {stock:<10} {category:<15}"
                )
        else:
            print("❌ No products found.")

        input("\nPress Enter to continue...")

    def update_product(self):
        """Update an existing product"""
        print("\n=== UPDATE PRODUCT ===")

        # First show all products
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM products ORDER BY id")
        products = cursor.fetchall()

        if not products:
            print("No products available to update.")
            input("\nPress Enter to continue...")
            return

        print("Available products:")
        for product_id, name in products:
            print(f"{product_id}. {name}")

        try:
            product_id = int(input("\nEnter product ID to update: "))

            # Check if product exists
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()

            if not product:
                print("❌ Product not found.")
                input("\nPress Enter to continue...")
                return

            print(f"\nUpdating product: {product[1]}")
            print("(Press Enter to keep current value)")

            # Get current values
            (
                current_name,
                current_desc,
                current_stock,
                current_price,
                current_category,
            ) = product[1:6]

            # Get new values with validation
            name_input = input(f"Name [{current_name}]: ").strip()
            name = (
                self.get_valid_input(f"Name [{current_name}]: ", "name")
                if name_input
                else current_name
            )

            desc_input = input(f"Description [{current_desc}]: ").strip()
            description = (
                self.get_valid_input(f"Description [{current_desc}]: ", "description")
                if desc_input
                else current_desc
            )

            stock_input = input(f"Stock [{current_stock}]: ").strip()
            stock = (
                self.get_valid_input(f"Stock [{current_stock}]: ", "stock")
                if stock_input
                else current_stock
            )

            price_input = input(f"Price [{current_price}]: ").strip()
            price = (
                self.get_valid_input(f"Price [{current_price}]: ", "price")
                if price_input
                else current_price
            )

            category_input = input(f"Category [{current_category}]: ").strip()
            category = (
                self.get_valid_input(f"Category [{current_category}]: ", "category")
                if category_input
                else current_category
            )

            # Update in database
            cursor.execute(
                """
                UPDATE products 
                SET name = ?, description = ?, stock = ?, price = ?, category = ?
                WHERE id = ?
                """,
                (name, description, stock, price, category, product_id),
            )
            self.connection.commit()

            print(f"✅ Product updated successfully!")

        except ValueError:
            print("❌ Invalid product ID.")

        input("\nPress Enter to continue...")

    def delete_product(self):
        """Delete a product from the database"""
        print("\n=== DELETE PRODUCT ===")

        # Show all products
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM products ORDER BY id")
        products = cursor.fetchall()

        if not products:
            print("No products available to delete.")
            input("\nPress Enter to continue...")
            return

        print("Available products:")
        for product_id, name in products:
            print(f"{product_id}. {name}")

        try:
            product_id = int(input("\nEnter product ID to delete: "))

            # Check if product exists
            cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()

            if not product:
                print("❌ Product not found.")
            else:
                confirm = input(
                    f"Are you sure you want to delete '{product[0]}'? (y/N): "
                ).lower()
                if confirm == "y":
                    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
                    self.connection.commit()
                    print(f"✅ Product '{product[0]}' deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")

        except ValueError:
            print("❌ Invalid product ID.")

        input("\nPress Enter to continue...")

    def generate_report(self):
        """Generate a summary report"""
        print("\n=== INVENTORY REPORT ===")

        cursor = self.connection.cursor()

        # Total products
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]

        # Total inventory value
        cursor.execute(
            "SELECT SUM(CAST(REPLACE(REPLACE(price, '$', ''), ' ', '') AS REAL) * stock) FROM products"
        )
        total_value = cursor.fetchone()[0] or 0

        # Low stock products (less than 10)
        cursor.execute(
            "SELECT COUNT(*) FROM products WHERE CAST(stock AS INTEGER) < 10"
        )
        low_stock_count = cursor.fetchone()[0]

        # Products by category
        cursor.execute("SELECT category, COUNT(*) FROM products GROUP BY category")
        categories = cursor.fetchall()

        print(f"Total Products: {total_products}")
        print(f"Total Inventory Value: ${total_value:.2f}")
        print(f"Low Stock Products: {low_stock_count}")

        if categories:
            print("\nProducts by Category:")
            for category, count in categories:
                print(f"  {category}: {count} products")

        input("\nPress Enter to continue...")

    def run(self):
        """Main application loop"""
        print("Welcome to Market Tech Dashboard!")

        while self.running:
            try:
                option = self.show_menu()

                if option == "1":
                    self.add_product()
                elif option == "2":
                    self.show_all_products()
                elif option == "3":
                    self.search_product()
                elif option == "4":
                    self.update_product()
                elif option == "5":
                    self.delete_product()
                elif option == "6":
                    self.generate_report()
                elif option == "7":
                    print("\n✅ Thank you for using Market Tech Dashboard!")
                    self.running = False
                else:
                    print("\n❌ Invalid option. Please try again.")
                    input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\n✅ Application terminated by user.")
                self.running = False
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("\nPress Enter to continue...")

        # Close database connection
        self.connection.close()


if __name__ == "__main__":
    dashboard = MarketDashboard()
    dashboard.run()
