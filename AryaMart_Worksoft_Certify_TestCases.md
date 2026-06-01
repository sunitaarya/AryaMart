# Worksoft Certify Automation Guide & Test Cases
### Application: AryaMart E-Commerce | Version: 1.0
### Automation Engine: Worksoft Certify - Web Interface Engine (HTML)

This document provides a highly structured, codeless **Worksoft Certify** automation definition. It maps out your Certify Application Map, Logical Object Definitions, and step-by-step Process Steps for all **12 modules (TP-01 to TP-12)** using the precise element IDs present in the AryaMart application.

---

## 1. Worksoft Certify Object Map (Application Map)

In Worksoft Certify, you first build an **Application Map** by capturing pages as **Windows** and elements as **Objects**. Configure your Certify Learn or Web Object Spy with the following physical identifiers:

| Logical Window | Logical Object | Physical Object Type | Physical Identifier (ID / Selector) |
| :--- | :--- | :--- | :--- |
| **Common_Header** | Logo | Link | `nav-logo` |
| | Nav_Home | Link | `nav-home` |
| | Nav_Products | Link | `nav-products` |
| | Nav_Orders | Link | `nav-orders` |
| | Nav_SearchOrder | Link | `nav-search-order` |
| | Cart_Badge | Web Element | `cart-badge` |
| | User_Menu_Btn | Button | `user-menu-btn` |
| | Logout_Item | Link | `dd-logout` |
| **Signup_Page** | Full_Name_Input | Text Box | `id=full_name` |
| | Username_Input | Text Box | `id=username` |
| | Email_Input | Text Box | `id=email` |
| | Phone_Input | Text Box | `id=phone` |
| | Password_Input | Text Box | `id=password` |
| | Confirm_Password_Input | Text Box | `id=confirm_password` |
| | Terms_Checkbox | Checkbox | `id=terms` |
| | Signup_Btn | Button | `id=signup-btn` |
| | Login_Link | Link | `goto-login` |
| | Strength_Bar | Web Element | `strength-bar` |
| **Login_Page** | Username_Input | Text Box | `id=username` |
| | Password_Input | Text Box | `id=password` |
| | Login_Btn | Button | `id=login-btn` |
| | Password_Toggle | Button | `id=toggle-password` |
| | Signup_Link | Link | `goto-signup` |
| **Home_Page** | Hero_Shop_Btn | Button | `hero-shop-btn` |
| | Hero_Join_Btn | Button | `hero-join-btn` |
| | Category_Pill | Link | `cat-1` (or custom attribute class) |
| **Products_Page** | Search_Input | Text Box | `id=search-input` |
| | Search_Submit_Btn | Button | `id=search-submit-btn` |
| | Clear_Search_Btn | Button | `id=clear-search-btn` |
| | Category_Filter | Dropdown | `id=category-filter` |
| | Sort_Filter | Dropdown | `id=sort-filter` |
| **Product_Detail** | Detail_Qty | Text Box / Number | `id=detail-qty` |
| | Qty_Increase | Button | `id=qty-increase` |
| | Qty_Decrease | Button | `id=qty-decrease` |
| | Add_To_Cart_Btn | Button | `id=detail-add-to-cart-btn` |
| | Login_To_Buy_Btn | Link | `id=detail-login-to-buy` |
| **Cart_Page** | Qty_Input | Text Box / Number | `id=qty-{id}` (e.g. dynamic loop) |
| | Qty_Increase_Btn | Button | `id=qty-inc-{id}` |
| | Qty_Decrease_Btn | Button | `id=qty-dec-{id}` |
| | Remove_Item_Btn | Link | `id=remove-item-{id}` |
| | Checkout_Btn | Button | `id=checkout-btn` |
| | Free_Shipping_Notice| Web Element | `id=free-shipping-notice` |
| | Free_Shipping_Done | Web Element | `id=free-shipping-achieved` |
| **Checkout_Page** | Shipping_Address | Text Box | `id=shipping_address` |
| | City_Input | Text Box | `id=city` |
| | State_Select | Dropdown | `id=state` |
| | Zip_Code_Input | Text Box | `id=zip_code` |
| | Place_Order_Btn | Button | `id=place-order-btn` |
| **Confirmation_Page**| Order_Number | Web Element | `id=confirmed-order-number` |
| | Conf_Status | Web Element | `id=conf-status-val` |
| | Conf_Amount | Web Element | `id=conf-amount-val` |
| | Conf_Address | Web Element | `id=conf-address-val` |
| | View_Orders_Btn | Button | `id=view-orders-btn` |
| **Orders_Page** | Search_Order_Link | Link | `search-order-link` |
| | Order_Card_Detail | Link | `id=view-order-{id}` |
| **Track_Order_Page**| Track_Input | Text Box | `id=order_number` |
| | Track_Btn | Button | `id=search-order-btn` |
| | Result_Order_No | Web Element | `id=result-order-number` |
| | Result_Status | Web Element | `id=result-status` |
| | Timeline_Step | Web Element | `id=timeline-{1-4}` |

---

## 2. Worksoft Certify Automated Processes (Test Packages)

Each process below represents a Certify process flow that you can parameterize using your Certify Recordset/Data Tables.

---

### TP-01: User Registration Process

*   **Certify Process Name**: `AryaMart_User_Registration`
*   **Logical Precondition**: Browser launched, navigated to `http://127.0.0.1:8888/signup`

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Signup_Page** | Full_Name_Input | `Set Text` | "Worksoft Automation User" |
| 2 | **Signup_Page** | Username_Input | `Set Text` | "worksoft_user" |
| 3 | **Signup_Page** | Email_Input | `Set Text` | "worksoft@aryamart.test" |
| 4 | **Signup_Page** | Phone_Input | `Set Text` | "+1-555-800-4968" |
| 5 | **Signup_Page** | Password_Input | `Set Text` | "Worksoft@1234" |
| 6 | **Signup_Page** | Confirm_Password_Input| `Set Text` | "Worksoft@1234" |
| 7 | **Signup_Page** | Terms_Checkbox | `Select` | `Checked` |
| 8 | **Signup_Page** | Signup_Btn | `Click` | |
| 9 | **Common_Header**| User_Menu_Btn | `Verify Attribute` | `Text Contains "Worksoft"` |

---

### TP-02: User Login Process

*   **Certify Process Name**: `AryaMart_User_Login`
*   **Logical Precondition**: Browser launched, navigated to `http://127.0.0.1:8888/login`

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Login_Page** | Username_Input | `Set Text` | "alice_j" |
| 2 | **Login_Page** | Password_Input | `Set Text` | "Alice@123" |
| 3 | **Login_Page** | Login_Btn | `Click` | |
| 4 | **Common_Header**| User_Menu_Btn | `Verify Attribute` | `Text Contains "Alice"` |

---

### TP-03: User Logout Process

*   **Certify Process Name**: `AryaMart_User_Logout`
*   **Logical Precondition**: User logged in (`AryaMart_User_Login` executed).

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Common_Header**| User_Menu_Btn | `Click` | |
| 2 | **Common_Header**| Logout_Item | `Click` | |
| 3 | **Login_Page** | Login_Btn | `Verify Property` | `Visible = True` |

---

### TP-04: Home Page Loading & Navigation

*   **Certify Process Name**: `AryaMart_Home_Navigation`
*   **Logical Precondition**: Navigated to `/home` (Logged out state).

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Home_Page** | Hero_Join_Btn | `Verify Property` | `Visible = True` |
| 2 | **Home_Page** | Hero_Shop_Btn | `Click` | |
| 3 | **Products_Page** | Search_Input | `Verify Property` | `Visible = True` |

---

### TP-05: Product Browsing and Search

*   **Certify Process Name**: `AryaMart_Product_Search_Filter`
*   **Logical Precondition**: Navigated to `/products`

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Products_Page** | Search_Input | `Set Text` | "Keyboard" |
| 2 | **Products_Page** | Search_Submit_Btn | `Click` | |
| 3 | **Products_Page** | Category_Filter | `Select` | "Electronics" |
| 4 | **Products_Page** | Sort_Filter | `Select` | "Price: Low to High" |
| 5 | **Products_Page** | Clear_Search_Btn | `Verify Property` | `Visible = True` |
| 6 | **Products_Page** | Clear_Search_Btn | `Click` | |

---

### TP-06: Product Detail & Quantity Selection

*   **Certify Process Name**: `AryaMart_Product_Detail_Verification`
*   **Logical Precondition**: Logged in, navigated to `/product/1`

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Product_Detail**| Qty_Increase | `Click` | |
| 2 | **Product_Detail**| Qty_Increase | `Click` | |
| 3 | **Product_Detail**| Detail_Qty | `Verify Attribute` | `Value = 3` |
| 4 | **Product_Detail**| Qty_Decrease | `Click` | |
| 5 | **Product_Detail**| Detail_Qty | `Verify Attribute` | `Value = 2` |
| 6 | **Product_Detail**| Add_To_Cart_Btn | `Click` | |

---

### TP-07: Add to Cart (Direct & Multi-item)

*   **Certify Process Name**: `AryaMart_Add_To_Cart_E2E`
*   **Logical Precondition**: Logged in.

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Common_Header**| Nav_Products | `Click` | |
| 2 | **Products_Page** | Search_Input | `Set Text` | "Water Bottle" |
| 3 | **Products_Page** | Search_Submit_Btn | `Click` | |
| 4 | **Products_Page** | Add_To_Cart_Btn | `Click` | (Add First Match) |
| 5 | **Common_Header**| Cart_Badge | `Verify Attribute` | `Text = 1` |

---

### TP-08: Cart Management & Shipping Logic

*   **Certify Process Name**: `AryaMart_Cart_Calculations`
*   **Logical Precondition**: Logged in, item in cart, navigated to `/cart`.

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Cart_Page** | Qty_Increase_Btn | `Click` | |
| 2 | **Cart_Page** | Free_Shipping_Done | `Verify Property` | `Visible = True` | (If total >= $50)
| 3 | **Cart_Page** | Checkout_Btn | `Click` | |

---

### TP-09: Checkout and Address Details

*   **Certify Process Name**: `AryaMart_Checkout_Details`
*   **Logical Precondition**: Cart has items, navigated to `/checkout`.

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Checkout_Page**| Shipping_Address | `Set Text` | "999 Certify Drive" |
| 2 | **Checkout_Page**| City_Input | `Set Text` | "Dallas" |
| 3 | **Checkout_Page**| State_Select | `Select` | "Texas" |
| 4 | **Checkout_Page**| Zip_Code_Input | `Set Text` | "75201" |
| 5 | **Checkout_Page**| Place_Order_Btn | `Click` | |

---

### TP-10: Order Confirmation Verification

*   **Certify Process Name**: `AryaMart_Order_Confirmation_Read`
*   **Logical Precondition**: Just placed an order, redirected to confirmation screen.

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Confirmation_Page**| Order_Number | `Get Value` | (Save to Certify Variable `{ORD_NUM}`) |
| 2 | **Confirmation_Page**| Conf_Status | `Verify Attribute` | `Text = Confirmed` |
| 3 | **Confirmation_Page**| View_Orders_Btn | `Click` | |

---

### TP-11: Order History Validation

*   **Certify Process Name**: `AryaMart_Order_History_Validation`
*   **Logical Precondition**: Navigated to `/orders` (Logged in as Alice).

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Orders_Page** | Search_Order_Link | `Verify Property` | `Visible = True` |
| 2 | **Orders_Page** | Order_Card_Detail | `Click` | (Verify alice's detail page loads) |

---

### TP-12: Search Order by Order Number (Track Order)

*   **Certify Process Name**: `AryaMart_Track_Order_Flow`
*   **Logical Precondition**: Logged in, order placed, have `{ORD_NUM}` Certify variable.

| Step | Window | Object | Action | Parameters / Inputs |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Common_Header**| Nav_SearchOrder | `Click` | |
| 2 | **Track_Order_Page**| Track_Input | `Set Text` | `{ORD_NUM}` |
| 3 | **Track_Order_Page**| Track_Btn | `Click` | |
| 4 | **Track_Order_Page**| Result_Order_No | `Verify Attribute` | `Text = {ORD_NUM}` |
| 5 | **Track_Order_Page**| Result_Status | `Verify Attribute` | `Text Contains Confirmed` |
| 6 | **Track_Order_Page**| Timeline_Step | `Verify Attribute` | `Class Contains active` (for step 2) |
