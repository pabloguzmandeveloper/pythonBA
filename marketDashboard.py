"""
Market Dashboard Application
Advanced product management system with validation
"""

import sqlite3

from appFeatures import (
    add_product,
    delete_product_from_db,
    get_all_products,
    get_inventory_value,
    get_low_stock_count,
    get_products_by_category,
    get_products_count,
    get_valid_input,
    search_product_by_id,
    search_products_by_category,
    search_products_by_name,
    update_product,
    update_product_in_db,
)


class MarketDashboard:
    """Initialize the application"""

    def __init__(self):
        self.running = True

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

    def show_all_products(self):
        """Display all products from database"""
        print("\n=== ALL PRODUCTS ===")

        products = get_all_products()

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
                    f"{product_id:<5} {name:<20} {description:<20} {price:<15} {stock:<10} {category:<15}"
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

        if option == "1":
            product_id = input("Enter product ID: ").strip()
            product = search_product_by_id(product_id)
            products = [product] if product else []
        elif option == "2":
            name = input("Enter product name (partial match): ").strip()
            products = search_products_by_name(name)
        elif option == "3":
            category = input("Enter category: ").strip()
            products = search_products_by_category(category)
        else:
            print("Invalid option.")
            input("\nPress Enter to continue...")
            return

        if products:
            print(f"\n✅ Found {len(products)} product(s):")
            print(
                f"{'ID':<5} {'Name':<20} {'Price':<15} {'Stock':<10} {'Category':<15}"
            )
            print("-" * 70)
            for product in products:
                product_id, name, description, stock, price, category = product
                print(
                    f"{product_id:<5} {name:<20} {description:<20} {price:<15} {stock:<10} {category:<15}"
                )
        else:
            print("❌ No products found.")

        input("\nPress Enter to continue...")

    def delete_product(self):
        """Delete a product from the database"""
        print("\n=== DELETE PRODUCT BY ID -- VERY DANGEROUS ===")

        # Show all products
        products = get_all_products()

        if not products:
            print("No products available to delete.")
            input("\nPress Enter to continue...")
            return

        print("Available products:")
        for product in products:
            product_id, name, _, _, _, _ = product
            print(f"{product_id}. {name}")

        # Get product ID with validation
        product_id = get_valid_input("\nEnter product ID to delete: ", "id")

        # Delete product using appFeatures function
        product_name, success = delete_product_from_db(product_id)

        if product_name:
            confirm = input(
                f"Are you sure you want to delete '{product_name}'? (y/N): "
            ).lower()
            if confirm == "y":
                if success:
                    print(f"✅ Product '{product_name}' deleted successfully!")
                else:
                    print("❌ Error deleting product.")
            else:
                print("❌ Deletion cancelled.")
        else:
            print("❌ Product not found.")

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
                    add_product()
                elif option == "2":
                    self.show_all_products()
                elif option == "3":
                    self.search_product()
                elif option == "4":
                    update_product()
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


if __name__ == "__main__":
    dashboard = MarketDashboard()
    dashboard.run()
