from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'petvista_secret_key'

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="petvista"
    )

# ─── HOME ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM products")
    total_products = cursor.fetchone()['total']
    cursor.execute("SELECT SUM(total_price) as revenue FROM sales")
    revenue = cursor.fetchone()['revenue'] or 0
    cursor.execute("SELECT COUNT(*) as sales_count FROM sales")
    sales_count = cursor.fetchone()['sales_count']
    cursor.execute("SELECT * FROM products WHERE quantity < 10 ORDER BY quantity ASC LIMIT 3")
    low_stock = cursor.fetchall()
    cursor.execute("""
        SELECT s.*, p.name as product_name 
        FROM sales s JOIN products p ON s.product_id = p.product_id 
        ORDER BY s.sale_date DESC LIMIT 5
    """)
    recent_sales = cursor.fetchall()
    conn.close()
    return render_template('index.html',
        total_products=total_products,
        revenue=revenue,
        sales_count=sales_count,
        low_stock=low_stock,
        recent_sales=recent_sales
    )

# ─── PRODUCTS ────────────────────────────────────────────────────────────────
@app.route('/products')
def products():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    if search:
        query += " AND name LIKE %s"
        params.append(f"%{search}%")
    if category:
        query += " AND category = %s"
        params.append(category)
    query += " ORDER BY name"
    cursor.execute(query, params)
    all_products = cursor.fetchall()
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
    categories = [r['category'] for r in cursor.fetchall()]
    conn.close()
    return render_template('products.html', products=all_products, categories=categories, search=search, selected_category=category)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO products (product_id, name, category, price, quantity) VALUES (%s,%s,%s,%s,%s)",
                (request.form['pid'], request.form['name'], request.form['category'],
                 float(request.form['price']), int(request.form['quantity']))
            )
            conn.commit()
            flash('Product added successfully! 🐾', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('products'))
    return render_template('add_product.html')

@app.route('/products/edit/<int:pid>', methods=['GET', 'POST'])
def edit_product(pid):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        try:
            cursor.execute(
                "UPDATE products SET price=%s, quantity=%s WHERE product_id=%s",
                (float(request.form['price']), int(request.form['quantity']), pid)
            )
            conn.commit()
            flash('Product updated! ✅', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        conn.close()
        return redirect(url_for('products'))
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (pid,))
    product = cursor.fetchone()
    conn.close()
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('products'))
    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<int:pid>', methods=['POST'])
def delete_product(pid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id=%s", (pid,))
    conn.commit()
    conn.close()
    flash('Product deleted.', 'success')
    return redirect(url_for('products'))

# ─── SELL ────────────────────────────────────────────────────────────────────
@app.route('/sell', methods=['GET', 'POST'])
def sell():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        pid = int(request.form['pid'])
        qty = int(request.form['quantity'])
        cursor.execute("SELECT name, price, quantity FROM products WHERE product_id=%s", (pid,))
        product = cursor.fetchone()
        if not product:
            flash('Product not found.', 'error')
        elif qty > product['quantity']:
            flash(f"Not enough stock. Only {product['quantity']} left.", 'error')
        else:
            total = qty * product['price']
            cursor.execute("UPDATE products SET quantity=%s WHERE product_id=%s", (product['quantity'] - qty, pid))
            cursor.execute(
                "INSERT INTO sales (product_id, quantity_sold, total_price, sale_date) VALUES (%s,%s,%s,%s)",
                (pid, qty, total, datetime.now())
            )
            conn.commit()
            flash(f"Sold {qty}x {product['name']} for ₹{total:.2f} 🎉", 'success')
        conn.close()
        return redirect(url_for('sell'))
    cursor.execute("SELECT * FROM products WHERE quantity > 0 ORDER BY name")
    products = cursor.fetchall()
    conn.close()
    return render_template('sell.html', products=products)

# ─── SALES ───────────────────────────────────────────────────────────────────
@app.route('/sales')
def sales():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, p.name as product_name, p.category
        FROM sales s JOIN products p ON s.product_id = p.product_id
        ORDER BY s.sale_date DESC
    """)
    all_sales = cursor.fetchall()
    cursor.execute("SELECT SUM(total_price) as total FROM sales")
    total_revenue = cursor.fetchone()['total'] or 0
    conn.close()
    return render_template('sales.html', sales=all_sales, total_revenue=total_revenue)

# ─── API: product lookup ──────────────────────────────────────────────────────
@app.route('/api/product/<int:pid>')
def api_product(pid):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (pid,))
    p = cursor.fetchone()
    conn.close()
    if p:
        return jsonify(p)
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
