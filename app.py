from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
import hashlib
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ecommerce_test_secret_key_2024"

DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")

# ─────────────────────────────────────────────
#  Database helpers
# ─────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    UNIQUE NOT NULL,
            email     TEXT    UNIQUE NOT NULL,
            password  TEXT    NOT NULL,
            full_name TEXT,
            phone     TEXT,
            created_at TEXT   DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            description TEXT,
            price       REAL    NOT NULL,
            category    TEXT,
            stock       INTEGER DEFAULT 100,
            image_url   TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity   INTEGER DEFAULT 1,
            FOREIGN KEY (user_id)    REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT    UNIQUE NOT NULL,
            user_id      INTEGER NOT NULL,
            total_amount REAL    NOT NULL,
            status       TEXT    DEFAULT 'Pending',
            shipping_address TEXT,
            created_at   TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id   INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity   INTEGER NOT NULL,
            price      REAL    NOT NULL,
            FOREIGN KEY (order_id)   REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Seed products if empty
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        products = [
            ("Wireless Headphones Pro",    "Premium noise-cancelling over-ear headphones with 40hr battery life.",    149.99, "Electronics",  50, "https://placehold.co/400x300/6366f1/white?text=Headphones"),
            ("Mechanical Keyboard RGB",    "Tactile 87-key mechanical keyboard with per-key RGB lighting.",           89.99,  "Electronics",  75, "https://placehold.co/400x300/8b5cf6/white?text=Keyboard"),
            ("Ergonomic Office Chair",     "Lumbar-support mesh chair with adjustable armrests and headrest.",        399.99, "Furniture",    20, "https://placehold.co/400x300/06b6d4/white?text=Chair"),
            ("Stainless Steel Water Bottle","Vacuum-insulated 32oz bottle keeps cold 24h / hot 12h.",                 29.99,  "Lifestyle",   200, "https://placehold.co/400x300/10b981/white?text=Bottle"),
            ("Smart Watch Series X",       "AMOLED smartwatch with GPS, heart-rate & SpO2 sensors.",                 249.99, "Electronics",  30, "https://placehold.co/400x300/f59e0b/white?text=SmartWatch"),
            ("Running Shoes Ultra",        "Lightweight carbon-plate running shoes for marathon training.",           179.99, "Footwear",     60, "https://placehold.co/400x300/ef4444/white?text=Shoes"),
            ("4K Webcam Studio",           "2160p webcam with built-in ring light and noise-cancelling mic.",         119.99, "Electronics",  40, "https://placehold.co/400x300/3b82f6/white?text=Webcam"),
            ("Yoga Mat Premium",           "6mm non-slip eco-friendly TPE mat with alignment lines.",                 45.99,  "Fitness",      90, "https://placehold.co/400x300/ec4899/white?text=YogaMat"),
            ("Portable Power Bank 20K",    "20,000mAh slim power bank with 65W fast charging and dual USB-C.",        59.99,  "Electronics",  80, "https://placehold.co/400x300/14b8a6/white?text=PowerBank"),
            ("Desk Lamp LED Smart",        "Touch-dimming LED desk lamp with USB charging port and 5 colour modes.",  39.99,  "Home",        120, "https://placehold.co/400x300/a855f7/white?text=DeskLamp"),
            ("Coffee Maker Deluxe",        "12-cup programmable drip coffee maker with thermal carafe.",              79.99,  "Kitchen",      35, "https://placehold.co/400x300/f97316/white?text=CoffeeMaker"),
            ("Bluetooth Speaker 360",      "360° omnidirectional waterproof speaker, 20W with 15h playback.",         69.99,  "Electronics",  55, "https://placehold.co/400x300/22c55e/white?text=Speaker"),
        ]
        c.executemany(
            "INSERT INTO products (name, description, price, category, stock, image_url) VALUES (?,?,?,?,?,?)",
            products
        )

    conn.commit()
    conn.close()


def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return user


def cart_count():
    uid = session.get("user_id")
    if not uid:
        return 0
    conn = get_db()
    row = conn.execute(
        "SELECT COALESCE(SUM(quantity),0) FROM cart WHERE user_id=?", (uid,)
    ).fetchone()
    conn.close()
    return row[0]


# ─────────────────────────────────────────────
#  Auth routes
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    conn = get_db()
    products = conn.execute("SELECT * FROM products LIMIT 8").fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM products").fetchall()
    conn.close()
    return render_template("home.html", products=products, categories=categories,
                           user=current_user(), cart_count=cart_count())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hash_password(password))
        ).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            flash("Welcome back, " + user["full_name"] + "!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html", user=current_user())


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username  = request.form.get("username",  "").strip()
        email     = request.form.get("email",     "").strip()
        phone     = request.form.get("phone",     "").strip()
        password  = request.form.get("password",  "")
        confirm   = request.form.get("confirm_password", "")

        if not all([full_name, username, email, password]):
            flash("Please fill in all required fields.", "error")
            return render_template("signup.html", user=None)
        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("signup.html", user=None)
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("signup.html", user=None)

        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO users (full_name, username, email, phone, password) VALUES (?,?,?,?,?)",
                (full_name, username, email, phone, hash_password(password))
            )
            conn.commit()
            user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
            conn.close()
            session["user_id"] = user["id"]
            flash("Account created successfully! Welcome, " + full_name + "!", "success")
            return redirect(url_for("home"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "error")
            conn.close()
    return render_template("signup.html", user=None)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ─────────────────────────────────────────────
#  Product routes
# ─────────────────────────────────────────────
@app.route("/products")
def products():
    query    = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    sort     = request.args.get("sort", "name")

    conn = get_db()
    sql  = "SELECT * FROM products WHERE 1=1"
    params = []
    if query:
        sql += " AND (name LIKE ? OR description LIKE ? OR category LIKE ?)"
        params += [f"%{query}%", f"%{query}%", f"%{query}%"]
    if category:
        sql += " AND category=?"
        params.append(category)

    sort_map = {"name": "name", "price_asc": "price ASC", "price_desc": "price DESC"}
    sql += f" ORDER BY {sort_map.get(sort, 'name')}"

    items      = conn.execute(sql, params).fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM products").fetchall()
    conn.close()
    return render_template("products.html", products=items, categories=categories,
                           query=query, selected_category=category, sort=sort,
                           user=current_user(), cart_count=cart_count())


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    conn    = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    related = conn.execute(
        "SELECT * FROM products WHERE category=? AND id!=? LIMIT 4",
        (product["category"], product_id)
    ).fetchall()
    conn.close()
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products"))
    return render_template("product_detail.html", product=product, related=related,
                           user=current_user(), cart_count=cart_count())


# ─────────────────────────────────────────────
#  Cart routes
# ─────────────────────────────────────────────
@app.route("/cart")
def cart():
    if not session.get("user_id"):
        flash("Please login to view your cart.", "warning")
        return redirect(url_for("login"))
    conn  = get_db()
    items = conn.execute("""
        SELECT c.id as cart_id, c.quantity, p.id as product_id,
               p.name, p.price, p.image_url
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id=?
    """, (session["user_id"],)).fetchall()
    conn.close()
    total = sum(i["price"] * i["quantity"] for i in items)
    return render_template("cart.html", items=items, total=total,
                           user=current_user(), cart_count=cart_count())


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    if not session.get("user_id"):
        flash("Please login to add items to cart.", "warning")
        return redirect(url_for("login"))
    product_id = int(request.form.get("product_id"))
    quantity   = int(request.form.get("quantity", 1))
    conn       = get_db()
    existing   = conn.execute(
        "SELECT * FROM cart WHERE user_id=? AND product_id=?",
        (session["user_id"], product_id)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE cart SET quantity=quantity+? WHERE id=?",
            (quantity, existing["id"])
        )
    else:
        conn.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?,?,?)",
            (session["user_id"], product_id, quantity)
        )
    conn.commit()
    conn.close()
    flash("Item added to cart!", "success")
    return redirect(request.referrer or url_for("products"))


@app.route("/cart/update", methods=["POST"])
def update_cart():
    cart_id  = int(request.form.get("cart_id"))
    quantity = int(request.form.get("quantity", 1))
    conn     = get_db()
    if quantity <= 0:
        conn.execute("DELETE FROM cart WHERE id=? AND user_id=?",
                     (cart_id, session["user_id"]))
    else:
        conn.execute("UPDATE cart SET quantity=? WHERE id=? AND user_id=?",
                     (quantity, cart_id, session["user_id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("cart"))


@app.route("/cart/remove/<int:cart_id>")
def remove_from_cart(cart_id):
    conn = get_db()
    conn.execute("DELETE FROM cart WHERE id=? AND user_id=?",
                 (cart_id, session["user_id"]))
    conn.commit()
    conn.close()
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart"))


# ─────────────────────────────────────────────
#  Checkout & Orders
# ─────────────────────────────────────────────
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not session.get("user_id"):
        flash("Please login to checkout.", "warning")
        return redirect(url_for("login"))
    conn  = get_db()
    items = conn.execute("""
        SELECT c.id as cart_id, c.quantity, p.id as product_id,
               p.name, p.price, p.image_url
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id=?
    """, (session["user_id"],)).fetchall()
    if not items:
        flash("Your cart is empty.", "warning")
        conn.close()
        return redirect(url_for("cart"))

    total = sum(i["price"] * i["quantity"] for i in items)

    if request.method == "POST":
        address  = request.form.get("shipping_address", "").strip()
        city     = request.form.get("city", "").strip()
        state    = request.form.get("state", "").strip()
        zip_code = request.form.get("zip_code", "").strip()
        full_address = f"{address}, {city}, {state} {zip_code}"

        if not all([address, city, state, zip_code]):
            flash("Please fill in all shipping details.", "error")
            conn.close()
            return render_template("checkout.html", items=items, total=total,
                                   user=current_user(), cart_count=cart_count())

        order_number = "ORD-" + str(uuid.uuid4())[:8].upper()
        conn.execute(
            "INSERT INTO orders (order_number, user_id, total_amount, status, shipping_address) VALUES (?,?,?,?,?)",
            (order_number, session["user_id"], total, "Confirmed", full_address)
        )
        order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        for item in items:
            conn.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?,?,?,?)",
                (order_id, item["product_id"], item["quantity"], item["price"])
            )

        conn.execute("DELETE FROM cart WHERE user_id=?", (session["user_id"],))
        conn.commit()
        conn.close()
        flash(f"Order placed successfully! Order Number: {order_number}", "success")
        return redirect(url_for("order_confirmation", order_number=order_number))

    conn.close()
    return render_template("checkout.html", items=items, total=total,
                           user=current_user(), cart_count=cart_count())


@app.route("/order/confirmation/<order_number>")
def order_confirmation(order_number):
    if not session.get("user_id"):
        return redirect(url_for("login"))
    conn  = get_db()
    order = conn.execute(
        "SELECT * FROM orders WHERE order_number=? AND user_id=?",
        (order_number, session["user_id"])
    ).fetchone()
    conn.close()
    return render_template("order_confirmation.html", order=order,
                           user=current_user(), cart_count=cart_count())


@app.route("/orders")
def orders():
    if not session.get("user_id"):
        flash("Please login to view your orders.", "warning")
        return redirect(url_for("login"))
    conn       = get_db()
    user_orders = conn.execute(
        "SELECT * FROM orders WHERE user_id=? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("orders.html", orders=user_orders,
                           user=current_user(), cart_count=cart_count())


@app.route("/orders/search", methods=["GET", "POST"])
def search_order():
    if not session.get("user_id"):
        flash("Please login to search orders.", "warning")
        return redirect(url_for("login"))
    result = None
    order_items_list = []
    if request.method == "POST":
        order_number = request.form.get("order_number", "").strip()
        conn  = get_db()
        result = conn.execute(
            "SELECT * FROM orders WHERE order_number=? AND user_id=?",
            (order_number, session["user_id"])
        ).fetchone()
        if result:
            order_items_list = conn.execute("""
                SELECT oi.quantity, oi.price, p.name, p.image_url
                FROM order_items oi JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id=?
            """, (result["id"],)).fetchall()
        conn.close()
        if not result:
            flash("No order found with that order number.", "error")
    return render_template("search_order.html", result=result, order_items=order_items_list,
                           user=current_user(), cart_count=cart_count())


@app.route("/order/<int:order_id>")
def order_detail(order_id):
    if not session.get("user_id"):
        return redirect(url_for("login"))
    conn  = get_db()
    order = conn.execute(
        "SELECT * FROM orders WHERE id=? AND user_id=?",
        (order_id, session["user_id"])
    ).fetchone()
    items = conn.execute("""
        SELECT oi.quantity, oi.price, p.name, p.image_url
        FROM order_items oi JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id=?
    """, (order_id,)).fetchall()
    conn.close()
    if not order:
        flash("Order not found or access denied.", "error")
        return redirect(url_for("orders"))
    return render_template("order_detail.html", order=order, items=items,
                           user=current_user(), cart_count=cart_count())


if __name__ == "__main__":
    init_db()
    print("\n" + "="*55)
    print("  AryaMart E-Commerce Test Application")
    print("  URL: http://127.0.0.1:8888")
    print("  Test credentials (after signup):")
    print("    Username: testuser | Password: test123")
    print("="*55 + "\n")
    app.run(debug=True, port=8888, use_reloader=False)
