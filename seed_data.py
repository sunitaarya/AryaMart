# -*- coding: utf-8 -*-
"""
seed_data.py -- Populate AryaMart with 20 dummy users + purchase history
Run once: python seed_data.py
"""

import sqlite3
import hashlib
import uuid
import os
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")

# ── helpers ──────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def rand_date(days_back: int = 180) -> str:
    dt = datetime.now() - timedelta(days=random.randint(0, days_back))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def order_num() -> str:
    return "ORD-" + str(uuid.uuid4())[:8].upper()

# ── dummy users ───────────────────────────────────────────────────────────────
USERS = [
    # (full_name,           username,       email,                        phone,          password)
    ("Alice Johnson",      "alice_j",      "alice@aryamart.test",        "+1-555-101-0001", "Alice@123"),
    ("Bob Martinez",       "bob_m",        "bob@aryamart.test",          "+1-555-101-0002", "Bob@1234"),
    ("Carol White",        "carol_w",      "carol@aryamart.test",        "+1-555-101-0003", "Carol@123"),
    ("David Brown",        "david_b",      "david@aryamart.test",        "+1-555-101-0004", "David@123"),
    ("Emma Davis",         "emma_d",       "emma@aryamart.test",         "+1-555-101-0005", "Emma@1234"),
    ("Frank Wilson",       "frank_w",      "frank@aryamart.test",        "+1-555-101-0006", "Frank@123"),
    ("Grace Lee",          "grace_l",      "grace@aryamart.test",        "+1-555-101-0007", "Grace@123"),
    ("Henry Taylor",       "henry_t",      "henry@aryamart.test",        "+1-555-101-0008", "Henry@123"),
    ("Isabella Thomas",    "isabella_t",   "isabella@aryamart.test",     "+1-555-101-0009", "Bella@123"),
    ("James Anderson",     "james_a",      "james@aryamart.test",        "+1-555-101-0010", "James@123"),
    ("Karen Jackson",      "karen_j",      "karen@aryamart.test",        "+1-555-101-0011", "Karen@123"),
    ("Liam Harris",        "liam_h",       "liam@aryamart.test",         "+1-555-101-0012", "Liam@1234"),
    ("Mia Clark",          "mia_c",        "mia@aryamart.test",          "+1-555-101-0013", "Mia@12345"),
    ("Noah Lewis",         "noah_l",       "noah@aryamart.test",         "+1-555-101-0014", "Noah@123"),
    ("Olivia Robinson",    "olivia_r",     "olivia@aryamart.test",       "+1-555-101-0015", "Olivia@12"),
    ("Peter Walker",       "peter_w",      "peter@aryamart.test",        "+1-555-101-0016", "Peter@123"),
    ("Quinn Hall",         "quinn_h",      "quinn@aryamart.test",        "+1-555-101-0017", "Quinn@123"),
    ("Rachel Young",       "rachel_y",     "rachel@aryamart.test",       "+1-555-101-0018", "Rachel@12"),
    ("Samuel King",        "samuel_k",     "samuel@aryamart.test",       "+1-555-101-0019", "Samuel@12"),
    ("Tina Scott",         "tina_s",       "tina@aryamart.test",         "+1-555-101-0020", "Tina@1234"),
]

# ── shipping addresses ────────────────────────────────────────────────────────
ADDRESSES = [
    "101 Maple Ave, Springfield, Illinois 62701",
    "202 Oak Street, Austin, Texas 73301",
    "303 Pine Rd, Seattle, Washington 98101",
    "404 Elm Blvd, Miami, Florida 33101",
    "505 Cedar Lane, Denver, Colorado 80201",
    "606 Birch Court, Boston, Massachusetts 02101",
    "707 Walnut Dr, Phoenix, Arizona 85001",
    "808 Chestnut St, Chicago, Illinois 60601",
    "909 Willow Way, Portland, Oregon 97201",
    "1010 Ash Ave, Nashville, Tennessee 37201",
    "1111 Spruce Blvd, Dallas, Texas 75201",
    "1212 Poplar Rd, San Jose, California 95101",
    "1313 Hickory Ln, Columbus, Ohio 43201",
    "1414 Magnolia Dr, Charlotte, North Carolina 28201",
    "1515 Sycamore St, Indianapolis, Indiana 46201",
    "1616 Redwood Ave, Las Vegas, Nevada 89101",
    "1717 Cypress Ct, Louisville, Kentucky 40201",
    "1818 Juniper Blvd, Memphis, Tennessee 38101",
    "1919 Laurel Way, Baltimore, Maryland 21201",
    "2020 Alder St, Milwaukee, Wisconsin 53201",
]

ORDER_STATUSES = ["Pending", "Confirmed", "Shipped", "Delivered"]

# ── weights so most orders are Confirmed/Delivered (more realistic) ───────────
STATUS_WEIGHTS = [0.05, 0.25, 0.30, 0.40]

def seed():
    conn = get_db()
    c = conn.cursor()

    # Fetch existing products
    products = c.execute("SELECT id, price FROM products").fetchall()
    if not products:
        print("[ERROR] No products found. Run app.py first to initialise the DB.")
        conn.close()
        return

    product_ids   = [p["id"]    for p in products]
    product_prices = {p["id"]: p["price"] for p in products}

    inserted_users = 0
    inserted_orders = 0
    inserted_items  = 0

    for i, (full_name, username, email, phone, password) in enumerate(USERS):
        # ── Insert user (skip if already exists) ──────────────────────────
        existing = c.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if existing:
            user_id = existing["id"]
            print(f"  [SKIP] User '{username}' already exists -- skipping user insert, still adding orders.")
        else:
            c.execute(
                "INSERT INTO users (full_name, username, email, phone, password) VALUES (?,?,?,?,?)",
                (full_name, username, email, phone, hash_password(password))
            )
            conn.commit()
            user_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
            inserted_users += 1

        address = ADDRESSES[i % len(ADDRESSES)]

        # ── Give each user 1–4 orders ─────────────────────────────────────
        num_orders = random.randint(1, 4)
        for _ in range(num_orders):
            status      = random.choices(ORDER_STATUSES, weights=STATUS_WEIGHTS)[0]
            created_at  = rand_date(180)
            # pick 1–5 distinct products per order
            num_products  = random.randint(1, 5)
            chosen_ids    = random.sample(product_ids, min(num_products, len(product_ids)))
            order_total   = 0.0
            line_items    = []
            for pid in chosen_ids:
                qty   = random.randint(1, 3)
                price = product_prices[pid]
                order_total += qty * price
                line_items.append((pid, qty, price))

            # Add shipping if < $50
            if order_total < 50:
                order_total += 5.99

            on = order_num()
            c.execute(
                """INSERT INTO orders
                   (order_number, user_id, total_amount, status, shipping_address, created_at)
                   VALUES (?,?,?,?,?,?)""",
                (on, user_id, round(order_total, 2), status, address, created_at)
            )
            order_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
            inserted_orders += 1

            for pid, qty, price in line_items:
                c.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?,?,?,?)",
                    (order_id, pid, qty, price)
                )
                inserted_items += 1

        # ── Add 1–3 items to the user's active cart ───────────────────────
        c.execute("DELETE FROM cart WHERE user_id=?", (user_id,))   # clear stale
        cart_products = random.sample(product_ids, random.randint(1, 3))
        for pid in cart_products:
            c.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (?,?,?)",
                (user_id, pid, random.randint(1, 2))
            )

    conn.commit()
    conn.close()

    print("\n" + "="*55)
    print("  [OK] Seed complete!")
    print(f"  [U]  Users inserted  : {inserted_users}")
    print(f"  [O]  Orders created  : {inserted_orders}")
    print(f"  [I]  Order items     : {inserted_items}")
    print("="*55)
    print("\nTest Credentials (Username / Password):")
    print("-"*60)
    print(f"  {'USERNAME':<20} {'PASSWORD':<20} {'FULL NAME'}")
    print("-"*60)
    for full_name, username, _, _, password in USERS:
        print(f"  {username:<20} {password:<20} {full_name}")
    print("-"*60 + "\n")

if __name__ == "__main__":
    seed()
