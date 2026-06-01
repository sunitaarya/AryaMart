# Tricentis Tosca Model-Based Automation Guide & Test Cases
### Project Name: AryaMart_Tosca_Automation | Version: 1.0
### Automation Engine: HTML / TBox Engine (Tricentis Tosca Commander)

This document provides a highly structured **Tricentis Tosca** automation specification. It outlines the **Model-Based Modules Map** and step-by-step **TestCase Hierarchies** (TP-01 to TP-12) for Tosca Commander using the specific element IDs of the AryaMart application.

---

## 1. Tricentis Tosca Module Mapping (TBox HTML Engine)

In Model-Based Test Automation (MBTA), you scan the pages using **Tosca XScan** to create **Modules**. Map your scanned controls to the following technical properties:

| Module / Screen Name | Control Name | Control Type | Technical Identifier (ID / OuterHTML) |
| :--- | :--- | :--- | :--- |
| **Header_Navbar** | Logo | Link | `id==nav-logo` |
| | Home_Link | Link | `id==nav-home` |
| | Products_Link | Link | `id==nav-products` |
| | Orders_Link | Link | `id==nav-orders` |
| | Search_Order_Link | Link | `id==nav-search-order` |
| | Cart_Icon | Link | `id==nav-cart` |
| | Cart_Badge | WebHtmlControl | `id==cart-badge` |
| | User_Dropdown | WebHtmlControl | `id==user-menu-btn` |
| | Logout_Link | Link | `id==dd-logout` |
| **Signup_Page** | FullName_Input | TextBox | `id==full_name` |
| | Username_Input | TextBox | `id==username` |
| | Email_Input | TextBox | `id==email` |
| | Phone_Input | TextBox | `id==phone` |
| | Password_Input | TextBox | `id==password` |
| | ConfirmPassword_Input| TextBox | `id==confirm_password` |
| | Terms_Checkbox | CheckBox | `id==terms` |
| | Signup_Button | Button | `id==signup-btn` |
| | Login_Link | Link | `id==goto-login` |
| | Strength_Bar | WebHtmlControl | `id==strength-bar` |
| **Login_Page** | Username_Input | TextBox | `id==username` |
| | Password_Input | TextBox | `id==password` |
| | Login_Button | Button | `id==login-btn` |
| | ShowHide_Toggle | Button | `id==toggle-password` |
| | Signup_Link | Link | `id==goto-signup` |
| **Home_Page** | Hero_Shop_Button | Button | `id==hero-shop-btn` |
| | Hero_Join_Button | Button | `id==hero-join-btn` |
| | Category_Pill | Link | `id==cat-1` (or custom selector) |
| **Products_Page** | Search_TextBox | TextBox | `id==search-input` |
| | Search_Button | Button | `id==search-submit-btn` |
| | Clear_Search_Btn | Button | `id==clear-search-btn` |
| | Category_Dropdown | ComboBox | `id==category-filter` |
| | Sort_Dropdown | ComboBox | `id==sort-filter` |
| **Product_Detail** | Detail_Qty | TextBox | `id==detail-qty` |
| | Qty_Inc | Button | `id==qty-increase` |
| | Qty_Dec | Button | `id==qty-decrease` |
| | AddToCart_Button | Button | `id==detail-add-to-cart-btn` |
| | LoginToBuy_Button | Link | `id==detail-login-to-buy` |
| **Cart_Page** | Qty_Input_Row | TextBox | `id==qty-{id}` |
| | Qty_Inc_Row | Button | `id==qty-inc-{id}` |
| | Qty_Dec_Row | Button | `id==qty-dec-{id}` |
| | Remove_Item_Row | Link | `id==remove-item-{id}` |
| | Checkout_Button | Button | `id==checkout-btn` |
| | Shipping_Notice | WebHtmlControl | `id==free-shipping-notice` |
| | Shipping_Achieved | WebHtmlControl | `id==free-shipping-achieved` |
| **Checkout_Page** | ShippingAddress_Input| TextBox | `id==shipping_address` |
| | City_Input | TextBox | `id==city` |
| | State_Dropdown | ComboBox | `id==state` |
| | ZipCode_Input | TextBox | `id==zip_code` |
| | PlaceOrder_Button | Button | `id==place-order-btn` |
| **Confirmation_Page**| Confirmed_Order_No | WebHtmlControl | `id==confirmed-order-number` |
| | Status_Text | WebHtmlControl | `id==conf-status-val` |
| | Amount_Text | WebHtmlControl | `id==conf-amount-val` |
| | Address_Text | WebHtmlControl | `id==conf-address-val` |
| | View_Orders_Button | Button | `id==view-orders-btn` |
| **Orders_Page** | Search_Order_Link | Link | `class==search-order-link` |
| | View_Details_Link | Link | `id==view-order-{id}` |
| **Track_Order_Page**| Search_Input | TextBox | `id==order_number` |
| | Track_Button | Button | `id==search-order-btn` |
| | Result_Order_No | WebHtmlControl | `id==result-order-number` |
| | Result_Status | WebHtmlControl | `id==result-status` |
| | Timeline_Step_1 | WebHtmlControl | `id==timeline-1` |
| | Timeline_Step_2 | WebHtmlControl | `id==timeline-2` |
| | Timeline_Step_3 | WebHtmlControl | `id==timeline-3` |
| | Timeline_Step_4 | WebHtmlControl | `id==timeline-4` |

---

## 2. Tosca TestCase Structure (TP-01 to TP-12)

In Tosca Commander, you drag-and-drop the Modules into your **TestCases** folder. The tables below show the required **TestStepValues** and **ActionModes**.

---

### TP-01: User Registration Signup

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Registration / TC-01_User_Signup`
*   **Step 1**: Open Browser `http://127.0.0.1:8888/signup`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Signup_Page** | FullName_Input | "Tosca Automation User" | `Input` | `String` |
| **Signup_Page** | Username_Input | "tosca_user" | `Input` | `String` |
| **Signup_Page** | Email_Input | "tosca@aryamart.test" | `Input` | `String` |
| **Signup_Page** | Phone_Input | "+1-555-777-1234" | `Input` | `String` |
| **Signup_Page** | Password_Input | "Tosca@1234" | `Input` | `String` |
| **Signup_Page** | ConfirmPassword_Input| "Tosca@1234" | `Input` | `String` |
| **Signup_Page** | Terms_Checkbox | "True" | `Input` | `Boolean` |
| **Signup_Page** | Signup_Button | "" (Click) | `Input` | `String` |
| **Header_Navbar**| User_Dropdown | "\*tosca\*" | `Verify` | `String` |

---

### TP-02: User Login

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Authentication / TC-02_User_Login`
*   **Step 1**: Open Browser `http://127.0.0.1:8888/login`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Login_Page** | Username_Input | "alice_j" | `Input` | `String` |
| **Login_Page** | Password_Input | "Alice@123" | `Input` | `String` |
| **Login_Page** | Login_Button | "" (Click) | `Input` | `String` |
| **Header_Navbar**| User_Dropdown | "\*Alice\*" | `Verify` | `String` |

---

### TP-03: User Logout

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Authentication / TC-03_User_Logout`
*   **Precondition**: Executed `TC-02_User_Login`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Header_Navbar**| User_Dropdown | "" (Click) | `Input` | `String` |
| **Header_Navbar**| Logout_Link | "" (Click) | `Input` | `String` |
| **Login_Page** | Login_Button | "" | `Verify` | `String` |

---

### TP-04: Home Page Navigation

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Navigation / TC-04_Home_Navigation`
*   **Precondition**: Navigated to `/home`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Home_Page** | Hero_Join_Button | "" | `Verify` | `String` | (Verifies guest state)
| **Home_Page** | Hero_Shop_Button | "" (Click) | `Input` | `String` |
| **Products_Page** | Search_TextBox | "" | `Verify` | `String` | (Verifies redirection)

---

### TP-05: Product Search & Filtering

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Products / TC-05_Search_Filter`
*   **Precondition**: Navigated to `/products`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Products_Page** | Search_TextBox | "Keyboard" | `Input` | `String` |
| **Products_Page** | Search_Button | "" (Click) | `Input` | `String` |
| **Products_Page** | Category_Dropdown | "Electronics" | `Input` | `String` |
| **Products_Page** | Sort_Dropdown | "Price: High to Low" | `Input` | `String` |
| **Products_Page** | Clear_Search_Btn | "" (Click) | `Input` | `String` |

---

### TP-06: Quantity Selection

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Products / TC-06_Quantity_Selection`
*   **Precondition**: Logged in, navigated to `/product/1`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Product_Detail**| Qty_Inc | "" (Click) | `Input` | `String` |
| **Product_Detail**| Qty_Inc | "" (Click) | `Input` | `String` |
| **Product_Detail**| Detail_Qty | "3" | `Verify` | `String` |
| **Product_Detail**| Qty_Dec | "" (Click) | `Input` | `String` |
| **Product_Detail**| Detail_Qty | "2" | `Verify` | `String` |

---

### TP-07: Adding items to Cart

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Cart / TC-07_Add_To_Cart`
*   **Precondition**: Logged in, navigated to `/products`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Products_Page** | Search_TextBox | "Headphones" | `Input` | `String` |
| **Products_Page** | Search_Button | "" (Click) | `Input` | `String` |
| **Products_Page** | AddToCart_Button | "" (Click) | `Input` | `String` | (First Item card)
| **Header_Navbar**| Cart_Badge | "1" | `Verify` | `String` |

---

### TP-08: Cart Management (Shipping Notice Logic)

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Cart / TC-08_Cart_Management`
*   **Precondition**: Item added to cart, navigated to `/cart`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Cart_Page** | Qty_Inc_Row | "" (Click) | `Input` | `String` |
| **Cart_Page** | Shipping_Achieved | "" | `Verify` | `String` | (Verify Free Shipping notice)
| **Cart_Page** | Checkout_Button | "" (Click) | `Input` | `String` |

---

### TP-09: Checkout Delivery Fields

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Checkout / TC-09_Checkout_Fields`
*   **Precondition**: Cart contains items, navigated to `/checkout`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Checkout_Page**| ShippingAddress_Input| "123 Tosca Way" | `Input` | `String` |
| **Checkout_Page**| City_Input | "Austin" | `Input` | `String` |
| **Checkout_Page**| State_Dropdown | "Texas" | `Input` | `String` |
| **Checkout_Page**| ZipCode_Input | "73301" | `Input` | `String` |
| **Checkout_Page**| PlaceOrder_Button | "" (Click) | `Input` | `String` |

---

### TP-10: Placed Order Confirmation (Buffering `{ORD_NUM}`)

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Checkout / TC-10_Order_Confirmation`
*   **Precondition**: Just clicked "Place Order" in `TC-09`
*   **Buffer explanation**: We capture the dynamic order number from the screen and store it into the Tosca dynamic buffer `ORD_NUM`.

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Confirmation_Page**| Confirmed_Order_No | `ORD_NUM` | `Buffer` | `String` |
| **Confirmation_Page**| Status_Text | "Confirmed" | `Verify` | `String` |
| **Confirmation_Page**| View_Orders_Button | "" (Click) | `Input` | `String` |

---

### TP-11: Order History Loading

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Orders / TC-11_Order_History`
*   **Precondition**: Navigated to `/orders`

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Orders_Page** | Search_Order_Link | "" | `Verify` | `String` | (Checks track link is present)
| **Orders_Page** | View_Details_Link | "" (Click) | `Input` | `String` | (Loads detail page)

---

### TP-12: Track Order using `{ORD_NUM}` and verifying the progress timeline

*   **Tosca TestCase Path**: `AryaMart_Tosca_Folder / Orders / TC-12_Track_Order`
*   **Precondition**: Navigated to `/orders/search`, buffer `ORD_NUM` exists.

| Module | Module Attribute | Value | ActionMode | DataType |
| :--- | :--- | :--- | :--- | :--- |
| **Track_Order_Page**| Search_Input | `{B[ORD_NUM]}` | `Input` | `String` | (Uses buffered order ID)
| **Track_Order_Page**| Track_Button | "" (Click) | `Input` | `String` |
| **Track_Order_Page**| Result_Order_No | `{B[ORD_NUM]}` | `Verify` | `String` | (Verifies correct order)
| **Track_Order_Page**| Result_Status | "Confirmed" | `Verify` | `String` |
| **Track_Order_Page**| Timeline_Step_1 | "\*done\*" (or checkmark) | `Verify` | `String` |
| **Track_Order_Page**| Timeline_Step_2 | "\*active\*" | `Verify` | `String` | (Pulsing step indicator)
