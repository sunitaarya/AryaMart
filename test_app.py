import os
import sqlite3
import unittest
import uuid
import re

# ─────────────────────────────────────────────────────────────────────────────
# Overrides: Direct DB to test_ecommerce.db before importing app or seed_data
# ─────────────────────────────────────────────────────────────────────────────
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "test_ecommerce.db")

import app
app.DB_PATH = TEST_DB_PATH

import seed_data
seed_data.DB_PATH = TEST_DB_PATH


class AryaMartTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Clean up any stale test database
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except PermissionError:
                pass

        # 2. Re-initialize and seed the test database
        app.init_db()
        seed_data.seed()

        # 3. Store max seeded IDs to quickly revert custom data in setUp()
        conn = sqlite3.connect(TEST_DB_PATH)
        c = conn.cursor()
        cls.max_seeded_order_id = c.execute("SELECT MAX(id) FROM orders").fetchone()[0] or 0
        cls.max_seeded_user_id = c.execute("SELECT MAX(id) FROM users").fetchone()[0] or 0
        conn.close()

        # 4. Set testing configurations
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False

    @classmethod
    def tearDownClass(cls):
        # Clean up test DB file after running all tests
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except PermissionError:
                pass

    def setUp(self):
        self.client = app.app.test_client()

        # Revert database to original clean seeded state
        conn = sqlite3.connect(TEST_DB_PATH)
        c = conn.cursor()
        # Delete custom users created during tests
        c.execute("DELETE FROM users WHERE id > ?", (self.max_seeded_user_id,))
        # Reset cart entirely
        c.execute("DELETE FROM cart")
        # Delete custom order items and orders
        c.execute("DELETE FROM order_items WHERE order_id > ?", (self.max_seeded_order_id,))
        c.execute("DELETE FROM orders WHERE id > ?", (self.max_seeded_order_id,))
        conn.commit()
        conn.close()

        # Reset session
        with self.client.session_transaction() as sess:
            sess.clear()

    # ─────────────────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────────────────
    def login(self, username, password):
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def signup(self, full_name, username, email, phone, password, confirm_password):
        return self.client.post('/signup', data={
            'full_name': full_name,
            'username': username,
            'email': email,
            'phone': phone,
            'password': password,
            'confirm_password': confirm_password
        }, follow_redirects=True)

    def add_to_cart(self, product_id, quantity=1):
        return self.client.post('/cart/add', data={
            'product_id': product_id,
            'quantity': quantity
        }, follow_redirects=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-01: User Registration (Signup)
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_01_01_successful_signup(self):
        """TC-01-01 | Successful New User Registration"""
        res = self.signup("Test User", "new_test_user", "newtest@aryamart.test", "+1-555-999-0001", "Test@1234", "Test@1234")
        html = res.data.decode('utf-8')
        
        self.assertIn("Account created successfully!", html)
        self.assertIn("Welcome, Test User!", html)
        # Check database persistence
        conn = sqlite3.connect(TEST_DB_PATH)
        user = conn.execute("SELECT * FROM users WHERE username='new_test_user'").fetchone()
        conn.close()
        self.assertIsNotNone(user)
        self.assertEqual(user[5], "+1-555-999-0001") # phone check (column index 5)

    def test_tc_01_02_signup_missing_fields(self):
        """TC-01-02 | Registration - Missing Required Fields"""
        res = self.signup("", "", "", "", "", "")
        self.assertIn("Please fill in all required fields.", res.data.decode('utf-8'))

    def test_tc_01_03_signup_password_mismatch(self):
        """TC-01-03 | Registration - Password Mismatch"""
        res = self.signup("Test User", "new_user_mismatch", "mismatch@aryamart.test", "", "Test@1234", "Wrong@1234")
        self.assertIn("Passwords do not match.", res.data.decode('utf-8'))

    def test_tc_01_04_signup_password_too_short(self):
        """TC-01-04 | Registration - Password Too Short"""
        res = self.signup("Test User", "new_user_short", "short@aryamart.test", "", "Ab1", "Ab1")
        self.assertIn("Password must be at least 6 characters.", res.data.decode('utf-8'))

    def test_tc_01_05_signup_duplicate_username(self):
        """TC-01-05 | Registration - Duplicate Username"""
        res = self.signup("New Alice", "alice_j", "alice_new@aryamart.test", "", "Alice@123", "Alice@123")
        self.assertIn("Username or email already exists.", res.data.decode('utf-8'))

    def test_tc_01_06_signup_duplicate_email(self):
        """TC-01-06 | Registration - Duplicate Email"""
        res = self.signup("New Alice", "alice_new_uname", "alice@aryamart.test", "", "Alice@123", "Alice@123")
        self.assertIn("Username or email already exists.", res.data.decode('utf-8'))

    def test_tc_01_07_password_strength_indicator_element(self):
        """TC-01-07 | Password Strength Indicator Elements in UI"""
        res = self.client.get('/signup')
        html = res.data.decode('utf-8')
        # Check strength bar layout and logic present in page source
        self.assertIn("strength-bar", html)
        self.assertIn("pw-strength-text", html)

    def test_tc_01_08_navigate_to_login_from_signup(self):
        """TC-01-08 | Navigate to Login from Signup Link"""
        res = self.client.get('/signup')
        html = res.data.decode('utf-8')
        self.assertIn('href="/login"', html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-02: User Login
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_02_01_successful_login(self):
        """TC-02-01 | Successful Login"""
        res = self.login("alice_j", "Alice@123")
        html = res.data.decode('utf-8')
        self.assertIn("Welcome back, Alice Johnson!", html)
        # Check active session
        with self.client.session_transaction() as sess:
            self.assertIsNotNone(sess.get('user_id'))

    def test_tc_02_02_login_wrong_password(self):
        """TC-02-02 | Login - Wrong Password"""
        res = self.login("alice_j", "wrongpassword")
        self.assertIn("Invalid username or password.", res.data.decode('utf-8'))

    def test_tc_02_03_login_non_existent_username(self):
        """TC-02-03 | Login - Non-Existent Username"""
        res = self.login("ghost_user", "Any@1234")
        self.assertIn("Invalid username or password.", res.data.decode('utf-8'))

    def test_tc_02_04_login_both_fields_blank(self):
        """TC-02-04 | Login - Both Fields Blank"""
        res = self.login("", "")
        self.assertIn("Invalid username or password.", res.data.decode('utf-8'))

    def test_tc_02_05_password_toggle_elements(self):
        """TC-02-05 | Password Show/Hide Toggle Element check"""
        res = self.client.get('/login')
        html = res.data.decode('utf-8')
        self.assertIn("toggle-password", html)

    def test_tc_02_06_navigate_to_signup_from_login(self):
        """TC-02-06 | Navigate to Signup from Login Link"""
        res = self.client.get('/login')
        html = res.data.decode('utf-8')
        self.assertIn('href="/signup"', html)

    def test_tc_02_07_access_protected_routes_unauthenticated(self):
        """TC-02-07 | Access Protected Routes Without Login"""
        routes = [('/cart', "Please login to view your cart."),
                  ('/orders', "Please login to view your orders."),
                  ('/checkout', "Please login to checkout.")]
        for path, flash_msg in routes:
            res = self.client.get(path, follow_redirects=True)
            self.assertIn(flash_msg, res.data.decode('utf-8'))

    # ─────────────────────────────────────────────────────────────────────────
    # TP-03: User Logout
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_03_01_successful_logout(self):
        """TC-03-01 | Successful Logout"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/logout', follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("You have been logged out.", html)
        with self.client.session_transaction() as sess:
            self.assertIsNone(sess.get('user_id'))

    def test_tc_03_02_cannot_access_protected_after_logout(self):
        """TC-03-02 | Cannot Access Protected Pages After Logout"""
        self.login("alice_j", "Alice@123")
        self.client.get('/logout')
        res = self.client.get('/cart', follow_redirects=True)
        self.assertIn("Please login to view your cart.", res.data.decode('utf-8'))

    def test_tc_03_03_dropdown_elements_present(self):
        """TC-03-03 | User Dropdown Menu Markup"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/home')
        html = res.data.decode('utf-8')
        self.assertIn("user-menu-btn", html)
        self.assertIn("/logout", html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-04: Home Page
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_04_01_home_page_loads_logged_out(self):
        """TC-04-01 | Home Page Loads - Logged Out"""
        res = self.client.get('/home')
        html = res.data.decode('utf-8')
        self.assertIn("Welcome to AryaMart", html)
        self.assertIn("Join Free", html) # Visible for guest users
        self.assertIn("Shop Now", html)

    def test_tc_04_02_home_page_loads_logged_in(self):
        """TC-04-02 | Home Page Loads - Logged In"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/home')
        html = res.data.decode('utf-8')
        self.assertNotIn("Join Free", html) # Hidden for logged in users
        self.assertIn("Alice", html) # First name split is shown in user-menu-btn
        self.assertIn("My Orders", html)

    def test_tc_04_03_root_redirects_to_home(self):
        """TC-04-03 | Root URL Redirects to Home"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.headers['Location'].endswith('/home'))

    def test_tc_04_04_category_pill_links_rendered(self):
        """TC-04-04 | Category Pill Navigation Rendering"""
        res = self.client.get('/home')
        html = res.data.decode('utf-8')
        self.assertIn('href="/products?category=Electronics"', html)
        self.assertIn('href="/products?category=Furniture"', html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-05: Product Browsing and Search
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_05_01_products_page_all_products(self):
        """TC-05-01 | Products Page - All Products"""
        res = self.client.get('/products')
        html = res.data.decode('utf-8')
        self.assertIn("12 products found", html)
        self.assertIn("Wireless Headphones Pro", html)

    def test_tc_05_02_search_by_name_valid_match(self):
        """TC-05-02 | Search by Name - Valid Match"""
        res = self.client.get('/products?q=headphones')
        html = res.data.decode('utf-8')
        self.assertIn("1 product found", html)
        self.assertIn("Wireless Headphones Pro", html)
        self.assertNotIn("Mechanical Keyboard RGB", html)

    def test_tc_05_03_search_by_category_name(self):
        """TC-05-03 | Search by Category Name in General Query"""
        res = self.client.get('/products?q=electronics')
        html = res.data.decode('utf-8')
        self.assertIn("6 products found", html) # Total seeded electronics
        self.assertIn("Wireless Headphones Pro", html)

    def test_tc_05_04_search_no_results(self):
        """TC-05-04 | Search - No Results"""
        res = self.client.get('/products?q=xyznotfound123')
        html = res.data.decode('utf-8')
        self.assertIn("0 products found", html)
        self.assertIn("No Products Found", html)

    def test_tc_05_05_filter_by_category_dropdown(self):
        """TC-05-05 | Filter by Category Dropdown"""
        res = self.client.get('/products?category=Fitness')
        html = res.data.decode('utf-8')
        self.assertIn("1 product found", html)
        self.assertIn("Yoga Mat Premium", html)
        self.assertNotIn("Wireless Headphones Pro", html)

    def test_tc_05_06_sort_by_price_ascending(self):
        """TC-05-06 | Sort by Price Ascending"""
        res = self.client.get('/products?sort=price_asc')
        html = res.data.decode('utf-8')
        # Standard prices: Bottle $29.99, Keyboard $89.99, Chair $399.99
        bottle_idx = html.find("Stainless Steel Water Bottle")
        keyboard_idx = html.find("Mechanical Keyboard RGB")
        chair_idx = html.find("Ergonomic Office Chair")
        self.assertTrue(bottle_idx < keyboard_idx < chair_idx)

    def test_tc_05_07_sort_by_price_descending(self):
        """TC-05-07 | Sort by Price Descending"""
        res = self.client.get('/products?sort=price_desc')
        html = res.data.decode('utf-8')
        bottle_idx = html.find("Stainless Steel Water Bottle")
        keyboard_idx = html.find("Mechanical Keyboard RGB")
        chair_idx = html.find("Ergonomic Office Chair")
        self.assertTrue(chair_idx < keyboard_idx < bottle_idx)

    def test_tc_05_08_sort_by_name_alphabetical(self):
        """TC-05-08 | Sort by Name A-Z"""
        res = self.client.get('/products?sort=name')
        html = res.data.decode('utf-8')
        # 4K Webcam starts with "4", Bluetooth Speaker starts with "B"
        webcam_idx = html.find("4K Webcam Studio")
        speaker_idx = html.find("Bluetooth Speaker 360")
        self.assertTrue(webcam_idx < speaker_idx)

    def test_tc_05_09_clear_search_button(self):
        """TC-05-09 | Clear Search Button Markup"""
        res = self.client.get('/products?q=headphones')
        html = res.data.decode('utf-8')
        self.assertIn("clear-search-btn", html)

    def test_tc_05_10_combined_search_and_category(self):
        """TC-05-10 | Combined Search and Category Filter"""
        res = self.client.get('/products?q=speaker&category=Electronics')
        html = res.data.decode('utf-8')
        self.assertIn("1 product found", html)
        self.assertIn("Bluetooth Speaker 360", html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-06: Product Detail Page
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_06_01_product_detail_page_loads(self):
        """TC-06-01 | Product Detail Page Loads Correctly"""
        res = self.client.get('/product/1')
        html = res.data.decode('utf-8')
        self.assertIn("Wireless Headphones Pro", html)
        self.assertIn("149.99", html)
        self.assertIn("Premium noise-cancelling", html)

    def test_tc_06_02_quantity_selector_elements(self):
        """TC-06-02 | Quantity Selector Controls Present"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/product/1')
        html = res.data.decode('utf-8')
        self.assertIn("qty-decrease", html)
        self.assertIn("qty-increase", html)
        self.assertIn("detail-qty", html)

    def test_tc_06_03_related_products_display(self):
        """TC-06-03 | Related Products Display"""
        res = self.client.get('/product/1') # Category: Electronics
        html = res.data.decode('utf-8')
        self.assertIn("Related Products", html)
        self.assertIn("Mechanical Keyboard RGB", html) # From same category

    def test_tc_06_04_add_to_cart_visible_when_logged_in(self):
        """TC-06-04 | Add to Cart Button - Logged In"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/product/1')
        html = res.data.decode('utf-8')
        self.assertIn("Add to Cart", html)
        self.assertNotIn("Login to Purchase", html)

    def test_tc_06_05_login_to_purchase_when_logged_out(self):
        """TC-06-05 | Login to Purchase - Not Logged In"""
        res = self.client.get('/product/1')
        html = res.data.decode('utf-8')
        self.assertIn("Login to Purchase", html)
        self.assertNotIn('type="submit">Add to Cart', html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-07: Add to Cart
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_07_01_add_single_item_from_list(self):
        """TC-07-01 | Add Single Item from Product Listing"""
        self.login("alice_j", "Alice@123")
        res = self.add_to_cart(2) # Mechanical Keyboard
        html = res.data.decode('utf-8')
        self.assertIn("Item added to cart!", html)
        
        # Check database
        conn = sqlite3.connect(TEST_DB_PATH)
        cart_row = conn.execute("SELECT * FROM cart WHERE user_id=1 AND product_id=2").fetchone()
        conn.close()
        self.assertIsNotNone(cart_row)
        self.assertEqual(cart_row[3], 1) # quantity = 1

    def test_tc_07_02_add_same_product_twice(self):
        """TC-07-02 | Add Same Product Twice - Quantity Increments"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(3)
        self.add_to_cart(3)
        
        conn = sqlite3.connect(TEST_DB_PATH)
        cart_row = conn.execute("SELECT * FROM cart WHERE user_id=1 AND product_id=3").fetchone()
        conn.close()
        self.assertEqual(cart_row[3], 2) # quantity = 2

    def test_tc_07_03_add_to_cart_without_login(self):
        """TC-07-03 | Add to Cart Without Login"""
        res = self.add_to_cart(1)
        self.assertIn("Please login to add items to cart.", res.data.decode('utf-8'))

    def test_tc_07_04_add_multiple_different_products(self):
        """TC-07-04 | Add Multiple Different Products"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(4)
        self.add_to_cart(5)
        self.add_to_cart(6)
        
        res = self.client.get('/cart')
        html = res.data.decode('utf-8')
        self.assertIn("Stainless Steel Water Bottle", html)
        self.assertIn("Smart Watch Series X", html)
        self.assertIn("Running Shoes Ultra", html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-08: Cart Management
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_08_01_cart_page_loads_with_items(self):
        """TC-08-01 | Cart Page Loads with Items"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        res = self.client.get('/cart')
        html = res.data.decode('utf-8')
        self.assertIn("Wireless Headphones Pro", html)
        self.assertIn("149.99", html)
        self.assertIn("cart-summary", html) # Changed from order-summary

    def test_tc_08_02_increase_item_quantity(self):
        """TC-08-02 | Increase Item Quantity"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        
        conn = sqlite3.connect(TEST_DB_PATH)
        cart_id = conn.execute("SELECT id FROM cart WHERE user_id=1 AND product_id=1").fetchone()[0]
        conn.close()

        res = self.client.post('/cart/update', data={'cart_id': cart_id, 'quantity': 3}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("449.97", html) # 149.99 * 3 = 449.97 subtotal check

    def test_tc_08_03_decrease_item_quantity(self):
        """TC-08-03 | Decrease Item Quantity"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 3)
        
        conn = sqlite3.connect(TEST_DB_PATH)
        cart_id = conn.execute("SELECT id FROM cart WHERE user_id=1 AND product_id=1").fetchone()[0]
        conn.close()

        res = self.client.post('/cart/update', data={'cart_id': cart_id, 'quantity': 2}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("299.98", html) # 149.99 * 2 = 299.98 subtotal check

    def test_tc_08_04_set_quantity_to_zero_removes_item(self):
        """TC-08-04 | Set Quantity to 0 - Item Removed"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        
        conn = sqlite3.connect(TEST_DB_PATH)
        cart_id = conn.execute("SELECT id FROM cart WHERE user_id=1 AND product_id=1").fetchone()[0]
        conn.close()

        res = self.client.post('/cart/update', data={'cart_id': cart_id, 'quantity': 0}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertNotIn("Wireless Headphones Pro", html)

    def test_tc_08_05_remove_item_via_delete_button(self):
        """TC-08-05 | Remove Item via Delete Button"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        
        conn = sqlite3.connect(TEST_DB_PATH)
        cart_id = conn.execute("SELECT id FROM cart WHERE user_id=1 AND product_id=1").fetchone()[0]
        conn.close()

        res = self.client.get(f'/cart/remove/{cart_id}', follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("Item removed from cart.", html)
        self.assertNotIn("Wireless Headphones Pro", html)

    def test_tc_08_06_empty_cart_state(self):
        """TC-08-06 | Empty Cart State"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/cart')
        html = res.data.decode('utf-8')
        self.assertIn("Your Cart is Empty", html)
        self.assertIn("Start Shopping", html)

    def test_tc_08_07_free_shipping_notice_under_threshold(self):
        """TC-08-07 | Free Shipping Notice - Order Under $50"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(10, 1) # Smart Desk Lamp $39.99
        res = self.client.get('/cart')
        html = res.data.decode('utf-8')
        self.assertIn("free-shipping-notice", html)
        self.assertIn("Add", html) # "🚚 Add $10.01 more for free shipping!"
        self.assertIn("$5.99", html) # Shipping charge

    def test_tc_08_08_free_shipping_notice_over_threshold(self):
        """TC-08-08 | Free Shipping Achieved - Order Over $50"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1) # Headphones $149.99
        res = self.client.get('/cart')
        html = res.data.decode('utf-8')
        self.assertIn("free-shipping-achieved", html)
        self.assertIn("FREE", html)

    def test_tc_08_09_continue_shopping_link_present(self):
        """TC-08-09 | Continue Shopping Link in Cart"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1) # Add an item so it renders full cart layout (and has continue shopping)
        res = self.client.get('/cart')
        html = res.data.decode('utf-8')
        self.assertIn("Continue Shopping", html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-09: Checkout and Place Order
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_09_01_successful_order_placement(self):
        """TC-09-01 | Successful Order Placement"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1) # Headphones
        
        # Submit checkout details
        res = self.client.post('/checkout', data={
            'shipping_address': '456 Test Blvd',
            'city': 'San Jose',
            'state': 'California',
            'zip_code': '95112'
        }, follow_redirects=True)
        
        html = res.data.decode('utf-8')
        self.assertIn("Order placed successfully!", html)
        
        # Check database
        conn = sqlite3.connect(TEST_DB_PATH)
        order = conn.execute("SELECT * FROM orders WHERE user_id=1 ORDER BY id DESC LIMIT 1").fetchone()
        conn.close()
        self.assertIsNotNone(order)
        self.assertEqual(order[4], "Confirmed")
        self.assertIn("456 Test Blvd", order[5])

    def test_tc_09_02_checkout_missing_street_address(self):
        """TC-09-02 | Checkout - Missing Street Address"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        res = self.client.post('/checkout', data={
            'shipping_address': '',
            'city': 'San Jose',
            'state': 'California',
            'zip_code': '95112'
        }, follow_redirects=True)
        self.assertIn("Please fill in all shipping details.", res.data.decode('utf-8'))

    def test_tc_09_03_checkout_missing_city(self):
        """TC-09-03 | Checkout - Missing City"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        res = self.client.post('/checkout', data={
            'shipping_address': '123 Elm St',
            'city': '',
            'state': 'California',
            'zip_code': '95112'
        }, follow_redirects=True)
        self.assertIn("Please fill in all shipping details.", res.data.decode('utf-8'))

    def test_tc_09_04_checkout_missing_state(self):
        """TC-09-04 | Checkout - Missing State"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        res = self.client.post('/checkout', data={
            'shipping_address': '123 Elm St',
            'city': 'San Jose',
            'state': '',
            'zip_code': '95112'
        }, follow_redirects=True)
        self.assertIn("Please fill in all shipping details.", res.data.decode('utf-8'))

    def test_tc_09_05_checkout_missing_zip_code(self):
        """TC-09-05 | Checkout - Missing ZIP Code"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        res = self.client.post('/checkout', data={
            'shipping_address': '123 Elm St',
            'city': 'San Jose',
            'state': 'California',
            'zip_code': ''
        }, follow_redirects=True)
        self.assertIn("Please fill in all shipping details.", res.data.decode('utf-8'))

    def test_tc_09_06_checkout_empty_cart(self):
        """TC-09-06 | Checkout - Empty Cart Redirect"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/checkout', follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("Your cart is empty.", html)

    def test_tc_09_07_back_to_cart_button_present(self):
        """TC-09-07 | Back to Cart Button in Checkout Page"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        res = self.client.get('/checkout')
        html = res.data.decode('utf-8')
        self.assertIn("Back to Cart", html)

    def test_tc_09_08_payment_fields_readonly(self):
        """TC-09-08 | Payment Fields Prefilled & Read-Only Check"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        res = self.client.get('/checkout')
        html = res.data.decode('utf-8')
        self.assertIn('readonly', html)
        self.assertIn('4242 4242 4242 4242', html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-10: Order Confirmation
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_10_01_confirmation_page_displays_correctly(self):
        """TC-10-01 | Confirmation Page Displays Correctly"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        self.client.post('/checkout', data={
            'shipping_address': '123 confirmation way',
            'city': 'San Jose',
            'state': 'California',
            'zip_code': '95112'
        })
        
        conn = sqlite3.connect(TEST_DB_PATH)
        order_number = conn.execute("SELECT order_number FROM orders WHERE user_id=1 ORDER BY id DESC LIMIT 1").fetchone()[0]
        conn.close()

        res = self.client.get(f'/order/confirmation/{order_number}')
        html = res.data.decode('utf-8')
        self.assertIn("Order Confirmed", html) # Checked correct title casing
        self.assertIn(order_number, html)
        self.assertIn("123 confirmation way", html)

    def test_tc_10_02_view_orders_from_confirmation(self):
        """TC-10-02 | View Orders Link in Confirmation Page"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        self.client.post('/checkout', data={'shipping_address':'A', 'city':'B', 'state':'C', 'zip_code':'D'})
        conn = sqlite3.connect(TEST_DB_PATH)
        order_number = conn.execute("SELECT order_number FROM orders WHERE user_id=1 ORDER BY id DESC").fetchone()[0]
        conn.close()
        
        res = self.client.get(f'/order/confirmation/{order_number}')
        html = res.data.decode('utf-8')
        self.assertIn("View My Orders", html)

    def test_tc_10_03_continue_shopping_from_confirmation(self):
        """TC-10-03 | Continue Shopping Link in Confirmation Page"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        self.client.post('/checkout', data={'shipping_address':'A', 'city':'B', 'state':'C', 'zip_code':'D'})
        conn = sqlite3.connect(TEST_DB_PATH)
        order_number = conn.execute("SELECT order_number FROM orders WHERE user_id=1 ORDER BY id DESC").fetchone()[0]
        conn.close()
        
        res = self.client.get(f'/order/confirmation/{order_number}')
        html = res.data.decode('utf-8')
        self.assertIn("Continue Shopping", html)

    def test_tc_10_04_cart_empty_after_order_placement(self):
        """TC-10-04 | Cart Empty After Order Placement"""
        self.login("alice_j", "Alice@123")
        self.add_to_cart(1, 1)
        self.client.post('/checkout', data={'shipping_address':'A', 'city':'B', 'state':'C', 'zip_code':'D'})
        
        res = self.client.get('/cart')
        html = res.data.decode('utf-8')
        self.assertIn("Your Cart is Empty", html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-11: Order History
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_11_01_orders_page_history_populated(self):
        """TC-11-01 | My Orders Page with Order History"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/orders')
        html = res.data.decode('utf-8')
        self.assertIn("My Orders", html)
        self.assertIn("ORD-", html) # check order numbers present

    def test_tc_11_02_view_order_detail_from_list(self):
        """TC-11-02 | View Order Detail from Orders List"""
        self.login("alice_j", "Alice@123")
        
        conn = sqlite3.connect(TEST_DB_PATH)
        order_id = conn.execute("SELECT id FROM orders WHERE user_id=1 LIMIT 1").fetchone()[0]
        conn.close()

        res = self.client.get(f'/order/{order_id}')
        html = res.data.decode('utf-8')
        self.assertIn("Order Details", html) # Changed from Items Ordered to Order Details
        self.assertIn("Order Summary", html)

    def test_tc_11_03_status_badge_colors(self):
        """TC-11-03 | Status Badge Check"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/orders')
        html = res.data.decode('utf-8')
        # Check standard statuses exist in elements
        self.assertTrue("Pending" in html or "Confirmed" in html or "Shipped" in html or "Delivered" in html)

    def test_tc_11_04_no_orders_state(self):
        """TC-11-04 | No Orders State for new user"""
        self.signup("Fresh User", "fresh_guy", "fresh@aryamart.test", "", "Test@1234", "Test@1234")
        # Ensure cart is cleared (done in setUp, but let's be sure new user has 0 orders)
        res = self.client.get('/orders')
        html = res.data.decode('utf-8')
        self.assertIn("No Orders Yet", html)
        self.assertIn("Browse Products", html)

    def test_tc_11_05_isolation_other_user_orders_inaccessible(self):
        """TC-11-05 | User Cannot See Another User's Orders"""
        # Find an order ID belonging to Alice (user_id = 1)
        conn = sqlite3.connect(TEST_DB_PATH)
        alice_order_id = conn.execute("SELECT id FROM orders WHERE user_id=1 LIMIT 1").fetchone()[0]
        conn.close()

        # Log in as Bob (user_id = 2)
        self.login("bob_m", "Bob@1234")
        
        # Attempt to access Alice's order detail page
        res = self.client.get(f'/order/{alice_order_id}', follow_redirects=True)
        html = res.data.decode('utf-8')
        # Should redirect back to /orders list with flash message
        self.assertIn("Order not found or access denied.", html)
        self.assertNotIn("Order Summary", html)

    def test_tc_11_06_search_order_link_present(self):
        """TC-11-06 | Search Order Link in Orders Page"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/orders')
        html = res.data.decode('utf-8')
        self.assertIn('href="/orders/search"', html)

    # ─────────────────────────────────────────────────────────────────────────
    # TP-12: Search Order by Order Number
    # ─────────────────────────────────────────────────────────────────────────
    def test_tc_12_01_successful_order_search(self):
        """TC-12-01 | Successful Order Search"""
        self.login("alice_j", "Alice@123")
        
        # Get one of Alice's order numbers
        conn = sqlite3.connect(TEST_DB_PATH)
        order_number = conn.execute("SELECT order_number FROM orders WHERE user_id=1 LIMIT 1").fetchone()[0]
        conn.close()

        res = self.client.post('/orders/search', data={'order_number': order_number}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("order-result", html)
        self.assertIn(order_number, html)

    def test_tc_12_02_delivery_timeline_display(self):
        """TC-12-02 | Delivery Timeline Display in Search Results"""
        self.login("alice_j", "Alice@123")
        conn = sqlite3.connect(TEST_DB_PATH)
        order_number = conn.execute("SELECT order_number FROM orders WHERE user_id=1 LIMIT 1").fetchone()[0]
        conn.close()

        res = self.client.post('/orders/search', data={'order_number': order_number}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("order-timeline", html)
        self.assertIn("timeline-step", html)

    def test_tc_12_03_order_items_listed_in_search_result(self):
        """TC-12-03 | Order Items Listed in Search Result"""
        self.login("alice_j", "Alice@123")
        conn = sqlite3.connect(TEST_DB_PATH)
        order_number = conn.execute("SELECT order_number FROM orders WHERE user_id=1 LIMIT 1").fetchone()[0]
        conn.close()

        res = self.client.post('/orders/search', data={'order_number': order_number}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("Items Ordered", html)

    def test_tc_12_04_search_invalid_order_number(self):
        """TC-12-04 | Search - Invalid Order Number"""
        self.login("alice_j", "Alice@123")
        res = self.client.post('/orders/search', data={'order_number': 'ORD-ZZZZZZZZ'}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("No order found with that order number.", html)
        self.assertNotIn("order-result", html)

    def test_tc_12_05_search_other_user_order_number(self):
        """TC-12-05 | Search - Another User's Order Number"""
        # Find Alice's order number
        conn = sqlite3.connect(TEST_DB_PATH)
        alice_order_number = conn.execute("SELECT order_number FROM orders WHERE user_id=1 LIMIT 1").fetchone()[0]
        conn.close()

        # Log in as Bob
        self.login("bob_m", "Bob@1234")
        
        # Try to search for Alice's order number
        res = self.client.post('/orders/search', data={'order_number': alice_order_number}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("No order found with that order number.", html)
        self.assertNotIn("order-result", html)

    def test_tc_12_06_search_empty_order_number(self):
        """TC-12-06 | Search - Empty Order Number Field"""
        self.login("alice_j", "Alice@123")
        res = self.client.post('/orders/search', data={'order_number': ''}, follow_redirects=True)
        html = res.data.decode('utf-8')
        self.assertIn("No order found with that order number.", html)

    def test_tc_12_07_back_to_orders_link_present(self):
        """TC-12-07 | Back to Orders Link in Search Page"""
        self.login("alice_j", "Alice@123")
        res = self.client.get('/orders/search')
        html = res.data.decode('utf-8')
        self.assertIn("My Orders", html) # Link is visible in empty search state


if __name__ == '__main__':
    unittest.main()
