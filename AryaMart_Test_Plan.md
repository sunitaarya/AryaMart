# AryaMart - Comprehensive Test Plan
### Application: AryaMart E-Commerce | Version: 1.0
### Environment: http://127.0.0.1:8888 | DB: SQLite (ecommerce.db)
### Prepared for: Worksoft / Tosca / UiPath Automation Testing

---

## Document Control

| Field | Value |
|---|---|
| Project | AryaMart E-Commerce GUI Test |
| Version | 1.0 |
| Date | 2026-06-01 |
| Test Types | Functional, Negative, Edge Case, UI Validation |
| Environment | Local - Flask + SQLite |
| Base URL | http://127.0.0.1:8888 |
| Browser | Chrome / Firefox / Edge |

---

## Test Scope

| Module | Area |
|---|---|
| TP-01 | User Registration (Signup) |
| TP-02 | User Login |
| TP-03 | User Logout |
| TP-04 | Home Page |
| TP-05 | Product Browsing and Search |
| TP-06 | Product Detail Page |
| TP-07 | Add to Cart |
| TP-08 | Cart Management |
| TP-09 | Checkout and Place Order |
| TP-10 | Order Confirmation |
| TP-11 | Order History |
| TP-12 | Search Order by Order Number |

---

## Test Data - Quick Reference

| Username | Password | Name |
|---|---|---|
| alice_j | Alice@123 | Alice Johnson |
| bob_m | Bob@1234 | Bob Martinez |
| emma_d | Emma@1234 | Emma Davis |
| new_user_test | Test@1234 | Test User (register fresh) |

Products available: IDs 1-12 (Electronics, Furniture, Footwear, Fitness, Home, Kitchen, Lifestyle)

---

## Priority Legend

| Level | Meaning |
|---|---|
| P1 | Critical / Blocker |
| P2 | High |
| P3 | Medium |
| P4 | Low |

---

# TP-01 - User Registration (Signup)

**URL:** /signup
**Element IDs:** signup-form, full_name, username, email, phone, password, confirm_password, terms, signup-btn

---

### TC-01-01 | Successful New User Registration
**Priority:** P1
**Preconditions:** User does not already exist. App running.
**Test Data:** Full Name=Test User | Username=new_user_test | Email=testuser@aryamart.test | Password=Test@1234

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to http://127.0.0.1:8888/signup | - | Signup page loads; #signup-form visible |
| 2 | Enter Full Name | full_name | "Test User" accepted |
| 3 | Enter Username | username | "new_user_test" accepted |
| 4 | Enter Email | email | "testuser@aryamart.test" accepted |
| 5 | Enter Phone | phone | "+1-555-999-0001" accepted |
| 6 | Enter Password | password | Masked input; strength bar appears |
| 7 | Enter Confirm Password | confirm_password | Masked input |
| 8 | Check Terms checkbox | terms | Checkbox is checked |
| 9 | Click Create Account | signup-btn | Redirects to /home |
| 10 | Observe flash message | #flash-container | Success: "Account created successfully! Welcome, Test User!" |
| 11 | Observe navbar | user-menu-btn | Shows user name in navbar |

**Actual Result:** ___________ **Status:** ___

---

### TC-01-02 | Registration - Missing Required Fields
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /signup | - | Page loads |
| 2 | Leave all fields blank | - | - |
| 3 | Click Create Account | signup-btn | Stays on /signup |
| 4 | Observe flash | #flash-container | Error: "Please fill in all required fields." |

**Actual Result:** ___________ **Status:** ___

---

### TC-01-03 | Registration - Password Mismatch
**Priority:** P1
**Test Data:** Password=Test@1234 | Confirm=Wrong@1234

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Fill all fields correctly | full_name, username, email | Fields populated |
| 2 | Enter password | password | Test@1234 |
| 3 | Enter different confirm | confirm_password | Wrong@1234 |
| 4 | Click submit | signup-btn | Stays on signup page |
| 5 | Observe flash | #flash-container | Error: "Passwords do not match." |

**Actual Result:** ___________ **Status:** ___

---

### TC-01-04 | Registration - Password Too Short
**Priority:** P1
**Test Data:** Password=Ab1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Fill all required fields | - | Fields populated |
| 2 | Enter short password | password | Ab1 |
| 3 | Enter same confirm | confirm_password | Ab1 |
| 4 | Click submit | signup-btn | Stays on signup page |
| 5 | Observe flash | #flash-container | Error: "Password must be at least 6 characters." |

**Actual Result:** ___________ **Status:** ___

---

### TC-01-05 | Registration - Duplicate Username
**Priority:** P1
**Test Data:** Username=alice_j (exists in DB)

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Fill all fields using alice_j as username | username | alice_j |
| 2 | Click submit | signup-btn | Stays on signup page |
| 3 | Observe flash | #flash-container | Error: "Username or email already exists." |

**Actual Result:** ___________ **Status:** ___

---

### TC-01-06 | Registration - Duplicate Email
**Priority:** P2
**Test Data:** Email=alice@aryamart.test (exists)

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Fill all fields with existing email | email | alice@aryamart.test |
| 2 | Click submit | signup-btn | Stays on signup page |
| 3 | Observe flash | #flash-container | Error: "Username or email already exists." |

**Actual Result:** ___________ **Status:** ___

---

### TC-01-07 | Password Strength Indicator
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /signup | - | Page loads |
| 2 | Type "abc" in password | password | Strength shows "Very Weak" (red) |
| 3 | Type "abcABC" | password | Strength shows "Fair" (amber) |
| 4 | Type "abcABC1" | password | Strength shows "Good" (blue) |
| 5 | Type "abcABC1@" | password | Strength shows "Strong" (green) |

**Actual Result:** ___________ **Status:** ___

---

### TC-01-08 | Navigate to Login from Signup
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /signup | - | Page loads |
| 2 | Click "Sign in" link | goto-login | Redirects to /login |

**Actual Result:** ___________ **Status:** ___

---

# TP-02 - User Login

**URL:** /login
**Element IDs:** login-form, username, password, login-btn, toggle-password, goto-signup

---

### TC-02-01 | Successful Login
**Priority:** P1
**Test Data:** Username=alice_j | Password=Alice@123

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to http://127.0.0.1:8888/login | - | Login page loads |
| 2 | Enter username | username | alice_j accepted |
| 3 | Enter password | password | Masked input |
| 4 | Click Sign In | login-btn | Redirects to /home |
| 5 | Observe flash | #flash-container | Success: "Welcome back, Alice Johnson!" |
| 6 | Observe navbar | user-menu-btn | Shows Alice in navbar |
| 7 | Observe cart badge | cart-badge | Cart count visible |

**Actual Result:** ___________ **Status:** ___

---

### TC-02-02 | Login - Wrong Password
**Priority:** P1
**Test Data:** Username=alice_j | Password=wrongpassword

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /login | - | Page loads |
| 2 | Enter username | username | alice_j |
| 3 | Enter wrong password | password | wrongpassword |
| 4 | Click submit | login-btn | Stays on /login |
| 5 | Observe flash | #flash-container | Error: "Invalid username or password." |

**Actual Result:** ___________ **Status:** ___

---

### TC-02-03 | Login - Non-Existent Username
**Priority:** P1
**Test Data:** Username=ghost_user | Password=Any@1234

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /login | - | Page loads |
| 2 | Enter non-existent username | username | ghost_user |
| 3 | Enter any password | password | Any@1234 |
| 4 | Click submit | login-btn | Stays on /login |
| 5 | Observe flash | #flash-container | Error: "Invalid username or password." |

**Actual Result:** ___________ **Status:** ___

---

### TC-02-04 | Login - Both Fields Blank
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /login | - | Page loads |
| 2 | Leave both fields blank | - | - |
| 3 | Click submit | login-btn | Stays on /login; no crash |
| 4 | Observe flash | #flash-container | Error: "Invalid username or password." |

**Actual Result:** ___________ **Status:** ___

---

### TC-02-05 | Password Show/Hide Toggle
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /login | - | Page loads |
| 2 | Type in password field | password | Password masked |
| 3 | Click eye icon | toggle-password | Password becomes visible |
| 4 | Click eye icon again | toggle-password | Password masked again |

**Actual Result:** ___________ **Status:** ___

---

### TC-02-06 | Navigate to Signup from Login
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /login | - | Page loads |
| 2 | Click "Create one here" | goto-signup | Redirects to /signup |

**Actual Result:** ___________ **Status:** ___

---

### TC-02-07 | Access Protected Routes Without Login
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart without login | - | Redirected to /login |
| 2 | Observe flash | #flash-container | Warning: "Please login to view your cart." |
| 3 | Navigate to /orders | - | Redirected to /login |
| 4 | Observe flash | #flash-container | Warning: "Please login to view your orders." |
| 5 | Navigate to /checkout | - | Redirected to /login |
| 6 | Observe flash | #flash-container | Warning: "Please login to checkout." |

**Actual Result:** ___________ **Status:** ___

---

# TP-03 - User Logout

**Element IDs:** user-menu-btn, user-dropdown, dd-logout

---

### TC-03-01 | Successful Logout
**Priority:** P1
**Preconditions:** Logged in as alice_j.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Click username in navbar | user-menu-btn | Dropdown menu opens |
| 2 | Click Logout | dd-logout | Redirected to /login |
| 3 | Observe flash | #flash-container | Info: "You have been logged out." |
| 4 | Observe navbar | - | Login/Sign Up buttons visible |

**Actual Result:** ___________ **Status:** ___

---

### TC-03-02 | Cannot Access Protected Pages After Logout
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Redirected to /login |
| 2 | Navigate to /orders | - | Redirected to /login |
| 3 | Navigate to /orders/search | - | Redirected to /login |
| 4 | Navigate to /checkout | - | Redirected to /login |

**Actual Result:** ___________ **Status:** ___

---

### TC-03-03 | Dropdown Closes on Outside Click
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Click username in navbar | user-menu-btn | Dropdown opens |
| 2 | Click anywhere outside dropdown | document body | Dropdown closes |

**Actual Result:** ___________ **Status:** ___

---

# TP-04 - Home Page

**URL:** /home
**Element IDs:** hero-section, hero-title, hero-badge, hero-shop-btn, category-list, product-grid, value-grid

---

### TC-04-01 | Home Page Loads - Logged Out
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to http://127.0.0.1:8888/home | - | Page loads without error |
| 2 | Verify hero badge | hero-badge | Text: "Welcome to AryaMart" |
| 3 | Verify hero title | hero-title | Contains "AryaMart" |
| 4 | Verify Shop Now button | hero-shop-btn | Visible, links to /products |
| 5 | Verify Join Free button | hero-join-btn | Visible when not logged in |
| 6 | Verify product grid | product-grid | At least 8 product cards rendered |
| 7 | Verify category pills | category-list | Category pills visible |
| 8 | Verify value cards | value-grid | 4 value proposition cards visible |

**Actual Result:** ___________ **Status:** ___

---

### TC-04-02 | Home Page Loads - Logged In
**Priority:** P2
**Preconditions:** Logged in as alice_j.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /home | - | Page loads |
| 2 | Verify Join Free button | hero-join-btn | NOT visible when logged in |
| 3 | Verify Add buttons on cards | atc-btn-{id} | "Add" buttons visible |
| 4 | Verify My Orders link | nav-orders | Visible in navbar |

**Actual Result:** ___________ **Status:** ___

---

### TC-04-03 | Root URL Redirects to Home
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to http://127.0.0.1:8888/ | - | Auto-redirected to /home |
| 2 | Verify URL | browser URL bar | URL shows /home |

**Actual Result:** ___________ **Status:** ___

---

### TC-04-04 | Category Pill Navigation
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /home | - | Page loads |
| 2 | Click "Electronics" pill | cat-1 | Navigates to /products?category=Electronics |
| 3 | Verify filtered results | products-grid | Only Electronics products shown |

**Actual Result:** ___________ **Status:** ___

---

# TP-05 - Product Browsing and Search

**URL:** /products
**Element IDs:** search-input, search-submit-btn, category-filter, sort-filter, products-grid, results-count, clear-search-btn, no-results

---

### TC-05-01 | Products Page - All Products
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /products | - | Page loads |
| 2 | Verify grid | products-grid | 12 product cards visible |
| 3 | Verify count | results-count | Shows "12 products found" |
| 4 | Verify search bar | search-input | Input field empty |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-02 | Search by Name - Valid Match
**Priority:** P1
**Test Data:** Search=headphones

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /products | - | Page loads |
| 2 | Type search term | search-input | "headphones" entered |
| 3 | Click Search | search-submit-btn | Filtered results shown |
| 4 | Verify results | products-grid | "Wireless Headphones Pro" card visible |
| 5 | Verify count | results-count | Shows "1 product found" |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-03 | Search by Category Name
**Priority:** P2
**Test Data:** Search=electronics

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Enter "electronics" in search | search-input | Text entered |
| 2 | Click Search | search-submit-btn | Results load |
| 3 | Verify results | products-grid | Multiple electronics products shown |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-04 | Search - No Results
**Priority:** P1
**Test Data:** Search=xyznotfound123

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Enter non-matching term | search-input | Text entered |
| 2 | Click Search | search-submit-btn | Page reloads |
| 3 | Verify empty state | no-results | "No Products Found" block visible |
| 4 | Verify count | results-count | Shows "0 products found" |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-05 | Filter by Category Dropdown
**Priority:** P1
**Test Data:** Category=Fitness

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /products | - | Page loads |
| 2 | Select "Fitness" | category-filter | Dropdown selects Fitness |
| 3 | Verify auto-submit | - | Page reloads automatically |
| 4 | Verify grid | products-grid | Only Fitness products visible |
| 5 | Verify selected value | category-filter | "Fitness" still selected |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-06 | Sort by Price Ascending
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /products | - | Page loads |
| 2 | Select "Price: Low to High" | sort-filter | Dropdown changes |
| 3 | Verify grid order | first product card | Lowest price product appears first |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-07 | Sort by Price Descending
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Select "Price: High to Low" | sort-filter | Dropdown changes |
| 2 | Verify grid order | first product card | Highest price (Chair $399.99) appears first |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-08 | Sort by Name A-Z
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Select "Sort: Name A-Z" | sort-filter | Dropdown changes |
| 2 | Verify first card | product-name-{id} | Alphabetically first product shown first |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-09 | Clear Search Button
**Priority:** P2
**Preconditions:** A search has been performed.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Perform any search | search-input + search-submit-btn | Filtered results shown |
| 2 | Click X clear button | clear-search-btn | Navigates to /products with no filters |
| 3 | Verify all products shown | products-grid | All 12 products visible |

**Actual Result:** ___________ **Status:** ___

---

### TC-05-10 | Combined Search and Category Filter
**Priority:** P2
**Test Data:** Search=speaker | Category=Electronics

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Enter "speaker" in search | search-input | Text entered |
| 2 | Select Electronics | category-filter | Category selected |
| 3 | Click Search | search-submit-btn | Page reloads |
| 4 | Verify result | products-grid | "Bluetooth Speaker 360" shown |

**Actual Result:** ___________ **Status:** ___

---

# TP-06 - Product Detail Page

**URL:** /product/id
**Element IDs:** detail-product-name, detail-product-price, detail-product-description, detail-stock, detail-qty, qty-decrease, qty-increase, detail-add-to-cart-btn, related-grid, breadcrumb

---

### TC-06-01 | Product Detail Page Loads Correctly
**Priority:** P1
**Test Data:** Navigate to /product/1 (Wireless Headphones Pro)

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /product/1 | - | Page loads |
| 2 | Verify product name | detail-product-name | "Wireless Headphones Pro" |
| 3 | Verify price | detail-product-price | "$149.99" |
| 4 | Verify description | detail-product-description | Description text visible |
| 5 | Verify stock indicator | detail-stock | Stock status shown |
| 6 | Verify breadcrumb | breadcrumb | Navigation path visible |
| 7 | Verify related products | related-grid | Up to 4 related product cards shown |

**Actual Result:** ___________ **Status:** ___

---

### TC-06-02 | Quantity Selector Controls
**Priority:** P2
**Preconditions:** Logged in. On /product/1.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Verify default qty | detail-qty | Shows 1 |
| 2 | Click + (increase) | qty-increase | Qty becomes 2 |
| 3 | Click + again | qty-increase | Qty becomes 3 |
| 4 | Click - (decrease) | qty-decrease | Qty becomes 2 |
| 5 | Click - to 1 | qty-decrease | Qty becomes 1 |
| 6 | Click - below 1 | qty-decrease | Qty stays at 1 (min) |

**Actual Result:** ___________ **Status:** ___

---

### TC-06-03 | Related Products Display
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /product/1 (Electronics) | - | Page loads |
| 2 | Verify related section | related-section | Section visible |
| 3 | Verify related products | related-grid | Up to 4 Electronics products, not product 1 |
| 4 | Click a related product | related-link-{id} | Navigates to that product detail page |

**Actual Result:** ___________ **Status:** ___

---

### TC-06-04 | Add to Cart Button - Logged In
**Priority:** P1
**Preconditions:** Logged in as alice_j. On /product/1.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Set qty to 2 | qty-increase | Qty shows 2 |
| 2 | Click "Add to Cart" | detail-add-to-cart-btn | Page redirects |
| 3 | Observe flash | #flash-container | Success: "Item added to cart!" |
| 4 | Observe cart badge | cart-badge | Count increased by 2 |

**Actual Result:** ___________ **Status:** ___

---

### TC-06-05 | Login to Purchase - Not Logged In
**Priority:** P1
**Preconditions:** Not logged in.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /product/1 | - | Page loads |
| 2 | Verify login button shown | detail-login-to-buy | "Login to Purchase" button visible |
| 3 | Verify Add to Cart hidden | detail-add-to-cart-btn | NOT visible |
| 4 | Click login to purchase | detail-login-to-buy | Redirected to /login |

**Actual Result:** ___________ **Status:** ___

---

# TP-07 - Add to Cart

**Element IDs:** atc-btn-{id}, atc-form-{id}, cart-badge

---

### TC-07-01 | Add Single Item from Product Listing
**Priority:** P1
**Preconditions:** Logged in as bob_m.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /products | - | Product grid loads |
| 2 | Note current cart badge count | cart-badge | Record count N |
| 3 | Click Add on product 2 | atc-btn-2 | Page reloads |
| 4 | Observe flash | #flash-container | Success: "Item added to cart!" |
| 5 | Verify cart badge | cart-badge | Count = N + 1 |

**Actual Result:** ___________ **Status:** ___

---

### TC-07-02 | Add Same Product Twice - Quantity Increments
**Priority:** P1
**Preconditions:** Logged in. Product 3 not in cart.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Add product 3 | atc-btn-3 | Flash: "Item added to cart!" |
| 2 | Add product 3 again | atc-btn-3 | Flash: "Item added to cart!" |
| 3 | Navigate to /cart | nav-cart | Cart page loads |
| 4 | Find product 3 row | cart-item-{id} | Single row for product 3 |
| 5 | Check quantity | qty-{cart_id} | Quantity shows 2 (not two rows) |

**Actual Result:** ___________ **Status:** ___

---

### TC-07-03 | Add to Cart Without Login
**Priority:** P1
**Preconditions:** Not logged in.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /products | - | Page loads |
| 2 | Verify buttons | - | "Login to Buy" links shown |
| 3 | Click "Login to Buy" | login-btn-{id} | Redirected to /login |

**Actual Result:** ___________ **Status:** ___

---

### TC-07-04 | Add Multiple Different Products
**Priority:** P2
**Preconditions:** Logged in.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Add product 4 | atc-btn-4 | Flash success |
| 2 | Add product 5 | atc-btn-5 | Flash success |
| 3 | Add product 6 | atc-btn-6 | Flash success |
| 4 | Navigate to /cart | - | Cart page loads |
| 5 | Count cart items | cart-items-section | 3 separate product rows visible |

**Actual Result:** ___________ **Status:** ___

---

# TP-08 - Cart Management

**URL:** /cart
**Element IDs:** cart-layout, cart-item-{id}, qty-{id}, qty-inc-{id}, qty-dec-{id}, remove-item-{id}, cart-item-subtotal-{id}, summary-total-val, checkout-btn, continue-shopping-btn, empty-cart, free-shipping-notice, free-shipping-achieved

---

### TC-08-01 | Cart Page Loads with Items
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Cart page loads |
| 2 | Verify cart items visible | cart-items-section | One or more rows visible |
| 3 | Verify item name | cart-item-name-{id} | Correct product name |
| 4 | Verify item price | cart-item-price-{id} | Price per unit shown |
| 5 | Verify subtotal | cart-item-subtotal-{id} | = price x quantity |
| 6 | Verify order summary | cart-summary | Subtotal, shipping, total visible |
| 7 | Verify checkout button | checkout-btn | Visible and clickable |

**Actual Result:** ___________ **Status:** ___

---

### TC-08-02 | Increase Item Quantity
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Page loads |
| 2 | Note current qty | qty-{X} | Shows 1 |
| 3 | Click + | qty-inc-{X} | Form auto-submits |
| 4 | Verify new qty | qty-{X} | Shows 2 |
| 5 | Verify subtotal | cart-item-subtotal-{X} | = price x 2 |
| 6 | Verify total | summary-total-val | Reflects new total |

**Actual Result:** ___________ **Status:** ___

---

### TC-08-03 | Decrease Item Quantity
**Priority:** P1
**Preconditions:** Item with qty=2 in cart.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Page loads |
| 2 | Click - | qty-dec-{id} | Form submits |
| 3 | Verify qty | qty-{id} | Shows 1 |
| 4 | Verify subtotal | cart-item-subtotal-{id} | = price x 1 |

**Actual Result:** ___________ **Status:** ___

---

### TC-08-04 | Set Quantity to 0 - Item Removed
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Page loads |
| 2 | Click - until qty=0 | qty-dec-{id} | - |
| 3 | Submit form | auto-submit | Page reloads |
| 4 | Verify item removed | cart-item-{id} | Row no longer present |

**Actual Result:** ___________ **Status:** ___

---

### TC-08-05 | Remove Item via Delete Button
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Page loads |
| 2 | Click remove icon | remove-item-{cart_id} | Navigates to /cart/remove/{id} |
| 3 | Verify flash | #flash-container | Info: "Item removed from cart." |
| 4 | Verify item gone | cart-items-section | Row removed |

**Actual Result:** ___________ **Status:** ___

---

### TC-08-06 | Empty Cart State
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart with no items | - | Page loads |
| 2 | Verify empty state | empty-cart | "Your Cart is Empty" block visible |
| 3 | Verify shopping button | start-shopping-btn | "Start Shopping" visible |
| 4 | Click Start Shopping | start-shopping-btn | Navigates to /products |

**Actual Result:** ___________ **Status:** ___

---

### TC-08-07 | Free Shipping Notice - Order Under $50
**Priority:** P2
**Test Data:** Yoga Mat $45.99 qty=1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Ensure cart total < $50 | - | - |
| 2 | Navigate to /cart | - | Page loads |
| 3 | Verify notice shown | free-shipping-notice | Amount needed for free shipping shown |
| 4 | Verify shipping cost | summary-shipping-val | Shows $5.99 |

**Actual Result:** ___________ **Status:** ___

---

### TC-08-08 | Free Shipping Achieved - Order Over $50
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Add items totaling >= $50 | - | - |
| 2 | Navigate to /cart | - | Page loads |
| 3 | Verify achievement notice | free-shipping-achieved | "You qualify for free shipping!" shown |
| 4 | Verify shipping cost | summary-shipping-val | Shows FREE |

**Actual Result:** ___________ **Status:** ___

---

### TC-08-09 | Continue Shopping Link
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Page loads |
| 2 | Click Continue Shopping | continue-shopping-btn | Navigates to /products |

**Actual Result:** ___________ **Status:** ___

---

# TP-09 - Checkout and Place Order

**URL:** /checkout
**Element IDs:** checkout-form, shipping_address, city, state, zip_code, card_number, card_expiry, card_cvv, place-order-btn, back-to-cart-btn

---

### TC-09-01 | Successful Order Placement
**Priority:** P1
**Preconditions:** Logged in. Cart has at least 1 item.
**Test Data:** Address=100 Test Street | City=New York | State=New York | ZIP=10001

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Cart page loads |
| 2 | Click Checkout | checkout-btn | Navigates to /checkout |
| 3 | Verify steps bar | checkout-steps | Steps bar visible |
| 4 | Verify items listed | checkout-items-list | All cart items shown |
| 5 | Verify totals | co-total-val | Correct grand total shown |
| 6 | Enter street address | shipping_address | "100 Test Street" |
| 7 | Enter city | city | "New York" |
| 8 | Select state | state | "New York" selected |
| 9 | Enter ZIP | zip_code | "10001" |
| 10 | Verify card fields | card_number | "4242 4242 4242 4242" (readonly) |
| 11 | Click Place Order | place-order-btn | Navigates to /order/confirmation/ORD-XXXXXXXX |
| 12 | Observe flash | #flash-container | Success: "Order placed successfully!" |

**Actual Result:** ___________ **Status:** ___

---

### TC-09-02 | Checkout - Missing Street Address
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /checkout | - | Page loads |
| 2 | Leave shipping_address blank | - | - |
| 3 | Fill city, state, ZIP | city, state, zip_code | Fields filled |
| 4 | Click Place Order | place-order-btn | Stays on /checkout |
| 5 | Observe flash | #flash-container | Error: "Please fill in all shipping details." |

**Actual Result:** ___________ **Status:** ___

---

### TC-09-03 | Checkout - Missing City
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Fill address and ZIP; leave City blank | - | - |
| 2 | Click Place Order | place-order-btn | Stays on /checkout |
| 3 | Observe flash | #flash-container | Error: "Please fill in all shipping details." |

**Actual Result:** ___________ **Status:** ___

---

### TC-09-04 | Checkout - Missing State
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Fill address, city, ZIP; leave State blank | state | No state selected |
| 2 | Click Place Order | place-order-btn | Stays on checkout |
| 3 | Observe flash | #flash-container | Error: "Please fill in all shipping details." |

**Actual Result:** ___________ **Status:** ___

---

### TC-09-05 | Checkout - Missing ZIP Code
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Fill address, city, state; leave ZIP blank | zip_code | Blank |
| 2 | Click Place Order | place-order-btn | Stays on checkout |
| 3 | Observe flash | #flash-container | Error: "Please fill in all shipping details." |

**Actual Result:** ___________ **Status:** ___

---

### TC-09-06 | Checkout - Empty Cart
**Priority:** P2
**Preconditions:** Logged in. Cart is empty.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate directly to /checkout | - | Redirect to /cart |
| 2 | Observe flash | #flash-container | Warning: "Your cart is empty." |

**Actual Result:** ___________ **Status:** ___

---

### TC-09-07 | Back to Cart Button
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /checkout | - | Page loads |
| 2 | Click "Back to Cart" | back-to-cart-btn | Navigates back to /cart |
| 3 | Verify cart items intact | cart-items-section | Items still in cart |

**Actual Result:** ___________ **Status:** ___

---

### TC-09-08 | Payment Fields Pre-filled and Read-Only
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /checkout | - | Page loads |
| 2 | Verify card number | card_number | Shows 4242 4242 4242 4242 (readonly) |
| 3 | Verify expiry | card_expiry | Shows 12/28 (readonly) |
| 4 | Verify CVV | card_cvv | Shows 123 (readonly) |
| 5 | Verify notice | payment-notice | "This is a test environment" notice shown |

**Actual Result:** ___________ **Status:** ___

---

# TP-10 - Order Confirmation

**URL:** /order/confirmation/order_number
**Element IDs:** confirmation-card, success-circle, confirmed-order-number, conf-status-val, conf-amount-val, conf-address-val, conf-date-val, view-orders-btn, continue-shopping-conf-btn

---

### TC-10-01 | Confirmation Page Displays Correctly
**Priority:** P1
**Preconditions:** Just placed an order (TC-09-01 done).

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Verify confirmation page loaded | confirmation-card | Card visible |
| 2 | Verify success animation | success-circle | Green circle with checkmark |
| 3 | Verify order number | confirmed-order-number | Format ORD-XXXXXXXX |
| 4 | Verify status | conf-status-val | Shows "Confirmed" |
| 5 | Verify amount | conf-amount-val | Matches expected total |
| 6 | Verify address | conf-address-val | Shows shipping address |
| 7 | Verify What Happens Next | what-next-box | Next-step items visible |
| 8 | Copy order number | confirmed-order-number | Store for use in TP-12 |

**Actual Result:** ___________ **Status:** ___

---

### TC-10-02 | View Orders from Confirmation
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Click "View My Orders" | view-orders-btn | Navigates to /orders |
| 2 | Verify new order visible | orders-list | Most recent order at top |

**Actual Result:** ___________ **Status:** ___

---

### TC-10-03 | Continue Shopping from Confirmation
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Click "Continue Shopping" | continue-shopping-conf-btn | Navigates to /products |

**Actual Result:** ___________ **Status:** ___

---

### TC-10-04 | Cart Empty After Order Placement
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /cart | - | Cart page loads |
| 2 | Verify empty state | empty-cart | "Your Cart is Empty" shown |
| 3 | Verify cart badge | cart-badge | Shows 0 |

**Actual Result:** ___________ **Status:** ___

---

# TP-11 - Order History

**URL:** /orders
**Element IDs:** orders-list, order-card-{id}, order-number-{id}, order-status-{id}, order-amount-{id}, order-date-{id}, view-order-{id}, no-orders

---

### TC-11-01 | My Orders Page with Order History
**Priority:** P1
**Preconditions:** Logged in as alice_j (has seeded orders).

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders | - | Page loads |
| 2 | Verify order cards | orders-list | One or more order-card-{id} visible |
| 3 | Verify order number | order-number-{id} | ORD-XXXXXXXX format |
| 4 | Verify status badge | order-status-{id} | Color-coded status shown |
| 5 | Verify amount | order-amount-{id} | Dollar amount shown |
| 6 | Verify date | order-date-{id} | Date visible |
| 7 | Verify sort order | first card | Most recent order first |

**Actual Result:** ___________ **Status:** ___

---

### TC-11-02 | View Order Detail from Orders List
**Priority:** P1

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders | - | Orders list loaded |
| 2 | Click "View Details" on first order | view-order-{id} | Navigates to /order/{id} |
| 3 | Verify order detail page | od-card | Order number, status, items, total visible |
| 4 | Verify ordered items | od-items-list | Products with qty, price shown |
| 5 | Verify shop again button | od-shop-again-btn | "Shop Again" button present |

**Actual Result:** ___________ **Status:** ___

---

### TC-11-03 | Status Badge Colors
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders | - | Orders listed |
| 2 | Find "Pending" order | order-status-{id} | Amber/yellow badge |
| 3 | Find "Confirmed" order | order-status-{id} | Green badge |
| 4 | Find "Shipped" order | order-status-{id} | Blue badge |
| 5 | Find "Delivered" order | order-status-{id} | Purple badge |

Note: Check multiple accounts from seed data to find all status types.

**Actual Result:** ___________ **Status:** ___

---

### TC-11-04 | No Orders State
**Priority:** P2
**Preconditions:** New user with no orders.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders | - | Page loads |
| 2 | Verify empty state | no-orders | "No Orders Yet" block visible |
| 3 | Verify browse button | start-shopping-orders-btn | "Browse Products" button visible |

**Actual Result:** ___________ **Status:** ___

---

### TC-11-05 | User Cannot See Another Users Orders
**Priority:** P1
**Preconditions:** Logged in as alice_j.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Note alice_j's first order ID from /orders | - | Record order ID e.g. 5 |
| 2 | Logout and login as bob_m | - | Logged in as bob |
| 3 | Navigate to /order/5 (alice's order) | - | Page loads |
| 4 | Verify isolation | od-card | Bob cannot see Alice's order |

**Actual Result:** ___________ **Status:** ___

---

### TC-11-06 | Search Order Link from Orders Page
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders | - | Page loads |
| 2 | Click "Search by Order Number" | search-order-link | Navigates to /orders/search |

**Actual Result:** ___________ **Status:** ___

---

# TP-12 - Search Order by Order Number

**URL:** /orders/search
**Element IDs:** search-order-form, order_number, search-order-btn, order-result, result-order-number, result-status, result-amount, result-address, result-date, order-timeline, timeline-1 to timeline-4, result-items-list, back-to-orders-btn

---

### TC-12-01 | Successful Order Search
**Priority:** P1
**Test Data:** Use a real ORD-XXXXXXXX from /orders page

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders/search | - | Search page loads |
| 2 | Verify search form | search-order-form | Input field and button visible |
| 3 | Enter valid order number | order_number | e.g. ORD-A1B2C3D4 |
| 4 | Click Track Order | search-order-btn | Page reloads with result |
| 5 | Verify result card | order-result | Result card visible |
| 6 | Verify order number | result-order-number | Matches entered order number |
| 7 | Verify status | result-status | e.g., "Confirmed" |
| 8 | Verify amount | result-amount | Dollar amount shown |
| 9 | Verify address | result-address | Shipping address shown |
| 10 | Verify date | result-date | Date shown |

**Actual Result:** ___________ **Status:** ___

---

### TC-12-02 | Delivery Timeline Display
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | After successful search | order-timeline | Timeline visible |
| 2 | Verify 4 steps present | timeline-1 to timeline-4 | Pending, Confirmed, Shipped, Delivered |
| 3 | For Confirmed order - timeline-2 | timeline-2 | Active (pulsing animation) |
| 4 | For Confirmed order - timeline-1 | timeline-1 | Shows checkmark (done) |
| 5 | For Confirmed order - timeline-3/4 | timeline-3, timeline-4 | Shows circle (not yet) |

**Actual Result:** ___________ **Status:** ___

---

### TC-12-03 | Order Items Listed in Result
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | After successful order search | result-items-section | "Items Ordered" section visible |
| 2 | Verify items listed | result-items-list | Products shown with name, qty, price |
| 3 | Verify item names | result-item-name-{n} | Correct product names |
| 4 | Verify item prices | result-item-price-{n} | Price = unit x qty |

**Actual Result:** ___________ **Status:** ___

---

### TC-12-04 | Search - Invalid Order Number
**Priority:** P1
**Test Data:** ORD-ZZZZZZZZ (does not exist)

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders/search | - | Page loads |
| 2 | Enter invalid order number | order_number | ORD-ZZZZZZZZ |
| 3 | Click Track Order | search-order-btn | Page reloads |
| 4 | Verify no result card | order-result | Result card NOT shown |
| 5 | Observe flash | #flash-container | Error: "No order found with that order number." |

**Actual Result:** ___________ **Status:** ___

---

### TC-12-05 | Search - Another Users Order Number
**Priority:** P1
**Preconditions:** Logged in as bob_m. Know alice_j's order number.

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders/search | - | Page loads |
| 2 | Enter alice's order number | order_number | Alice's ORD number |
| 3 | Click Track Order | search-order-btn | Page reloads |
| 4 | Verify no result shown | order-result | Result card NOT shown |
| 5 | Observe flash | #flash-container | Error: "No order found with that order number." |

**Actual Result:** ___________ **Status:** ___

---

### TC-12-06 | Search - Empty Order Number Field
**Priority:** P2

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | Navigate to /orders/search | - | Page loads |
| 2 | Leave order number blank | order_number | Empty |
| 3 | Click Track Order | search-order-btn | Page reloads |
| 4 | Verify no result | order-result | No result card shown |
| 5 | Observe flash | #flash-container | Error: "No order found with that order number." |

**Actual Result:** ___________ **Status:** ___

---

### TC-12-07 | Back to Orders Link
**Priority:** P3

| Step | Action | Element | Expected Result |
|---|---|---|---|
| 1 | After any search | result-actions | "All Orders" button visible |
| 2 | Click "All Orders" | back-to-orders-btn | Navigates to /orders |

**Actual Result:** ___________ **Status:** ___

---

# Test Execution Summary

| Module | Total TCs | Passed | Failed | Skipped | Pass % |
|---|---|---|---|---|---|
| TP-01 Signup | 8 | | | | |
| TP-02 Login | 7 | | | | |
| TP-03 Logout | 3 | | | | |
| TP-04 Home Page | 4 | | | | |
| TP-05 Search and Browse | 10 | | | | |
| TP-06 Product Detail | 5 | | | | |
| TP-07 Add to Cart | 4 | | | | |
| TP-08 Cart Management | 9 | | | | |
| TP-09 Checkout | 8 | | | | |
| TP-10 Confirmation | 4 | | | | |
| TP-11 Order History | 6 | | | | |
| TP-12 Search Order | 7 | | | | |
| TOTAL | 75 | | | | |

---

# Defect Log

| Defect ID | TC ID | Title | Priority | Steps to Reproduce | Expected | Actual | Status |
|---|---|---|---|---|---|---|---|
| DEF-001 | | | | | | | Open |

---

# Environment Checklist

- [ ] Flask app running at http://127.0.0.1:8888
- [ ] ecommerce.db exists with 20 users seeded
- [ ] 12 products in DB
- [ ] All 20 user accounts accessible with credentials
- [ ] Browser cookies cleared before session tests
- [ ] Test Tool (Worksoft/Tosca/UIPath) connected to http://127.0.0.1:8888
