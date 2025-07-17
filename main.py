import mysql.connector
from datetime import datetime

# MySQL connection

conn = mysql.connector.connect(
    host="localhost",
    user="root",            
    password="root",
    database="petvista")
cursor = conn.cursor()

# Add Product

def add_product():
    pid = int(input("Enter product ID: "))
    name = input("Enter product name: ")
    category = input("Enter category (e.g.: Food, Grooming, Toys etc.): ")
    price = float(input("Enter price of the product: "))
    quantity = int(input("Enter quantity in stock: "))
    cursor.execute("INSERT INTO products VALUES (%s,%s,%s,%s,%s)",(pid,name,category,price,quantity))
    conn.commit()
    print("✅ Product added successfully.\n")

# View Products

def view_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print("\n🧾 Product Inventory:")
    for p in products:
        print(f"\nID: {p[0]} | Name: {p[1]} | Category: {p[2]} | Price: ₹{p[3]} | Qty: {p[4]}")
    print()

# Search Product

def search_product():
    keyword = input("Enter product name to search: ")
    cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{keyword}%",))
    results = cursor.fetchall()

    if not results:
        print("❌ No matching products found.\n")
    else:
        print("\n🔍 Search Results:")
        for p in results:
            print(f"ID: {p[0]}, Name: {p[1]}, Category: {p[2]}, Price: ₹{p[3]}, Qty: {p[4]}")
        print()

# Sell Product

def sell_product():
    pid = int(input("Enter product ID to sell: "))
    qty = int(input("Enter quantity to sell: "))

    cursor.execute("SELECT name, price, quantity FROM products WHERE product_id = %s", (pid,))#pid, makes at tuple with only one element
    product = cursor.fetchone()

    if product:
        name, price, stock = product

        if qty > stock:
            print("❌ Not enough stock.\n")
        else:
            total = qty * price
            new_qty = stock - qty

            # Update stock in products table
            cursor.execute("UPDATE products SET quantity = %s WHERE product_id = %s", (new_qty, pid))

            # Record sale in sales table
            cursor.execute(
                "INSERT INTO sales (product_id, quantity_sold, total_price, sale_date) VALUES (%s, %s, %s, %s)",
                (pid, qty, total, datetime.now())
            )

            conn.commit()

            print(f"\n✅ Sold {qty} x {name}")
            print(f"💰 Total: ₹{total}")
            print(f"📦 Stock left: {new_qty}\n")

    else:
        print("❌ Product not found.\n")

    
    print()
    
# View Sales

def view_sales():
    cursor.execute("SELECT * FROM sales ORDER BY sale_date DESC")
    sales = cursor.fetchall()

    print("\n📜 Sales History:")
      
    for s in sales:
        print(f"ID: {s[1]}|Date: {s[4]}|Quantity sold: {s[2]}|Total price: {s[3]}")
    print()

# Update Product
    
def update_product():
    
    pid = int(input("Enter product ID to update: "))
    print("1. Update Price")
    print("2. Update Quantity")
    choice = int(input("Enter choice (1/2): "))
    if choice == 1:
        new_price = input("Enter new price: ")
        cursor.execute("UPDATE products SET price = %s WHERE product_id = %s", (new_price, pid))
        conn.commit()
        print("✅ Price updated.\n")
        
    elif choice == 2:
        new_qty = input("Enter new quantity: ")
        cursor.execute("UPDATE products SET quantity = %s WHERE product_id = %s", (new_qty, pid))
        conn.commit()
        print("✅ Quantity updated.\n")
        
        
    else:
        print("❌ Invalid choice.\n")   
    print()    

# Delete Product

def delete_product():
    pid = int(input("Enter product ID to delete: "))
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (pid,))
    product = cursor.fetchone()

    if product:
        cursor.execute("DELETE FROM products WHERE product_id = %s", (pid,))
        conn.commit()
        print("✅ Product deleted successfully.\n")
    else:
        print("❌ Product not found.\n")
    print()

# Main Menu

def main():
    while True:
        print("========== 🐾 PetVista 🐾 ===========")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Sell Product")
        print("5. View Sales History")
        print("6. Update Product")
        print("7. Delete Product")
        print("8. Exit")
        print("=====================================\n")
        choice = input("Enter your choice (1–8): ")

        if choice == '1':
            add_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            search_product()
        elif choice == '4':
            sell_product()
        elif choice == '5':
            view_sales()
        elif choice == '6':
            update_product()
        elif choice == '7':
            delete_product()
        elif choice == '8':
            print("👋 Thank you for using PetVista!")
            break
        else:
            print("❌ Invalid choice. Try again.\n")

    conn.close()

main()

