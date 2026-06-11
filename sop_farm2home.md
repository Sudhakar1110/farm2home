# STANDARD OPERATING PROCEDURE (SOP)
## Farm2Home — Farm-to-Home Subscription Platform
### Built on Frappe Framework v15+ / ERPNext v15+

---

**Document Version:** 1.0.0  
**App Version:** 1.0.0  
**App Name:** farm2home  
**Module Name:** Farm to Home  
**Author:** Farm2Home Team  
**Last Updated:** June 2026  

---

## TABLE OF CONTENTS

1. [SYSTEM OVERVIEW](#1-system-overview)
2. [MODULES & ARCHITECTURE](#2-modules--architecture)
3. [ROLES & PERMISSIONS](#3-roles--permissions)
4. [DOCTYPES & DATA DICTIONARY](#4-doctypes--data-dictionary)
5. [WORKFLOWS](#5-workflows)
6. [AUTOMATED SCHEDULED TASKS](#6-automated-scheduled-tasks)
7. [DOCUMENT EVENTS (HOOKS)](#7-document-events-hooks)
8. [API ENDPOINTS](#8-api-endpoints)
9. [REPORTS & DASHBOARDS](#9-reports--dashboards)
10. [NOTIFICATIONS](#10-notifications)
11. [PRINT FORMATS](#11-print-formats)
12. [WEB FORMS](#12-web-forms)
13. [INSTALLATION & SETUP](#13-installation--setup)
14. [DATA GENERATION (DEMO/TEST)](#14-data-generation-demo-test)
15. [PATCHES & MIGRATIONS](#15-patches--migrations)
16. [BACKUP & RESTORE](#16-backup--restore)
17. [TROUBLESHOOTING](#17-troubleshooting)
18. [APPENDIX](#18-appendix)

---

## 1. SYSTEM OVERVIEW

### 1.1 Purpose
Farm2Home is a comprehensive farm-to-home subscription marketplace built on Frappe Framework v15+ and ERPNext v15+. The platform connects farmers directly with consumers, enabling subscription-based recurring deliveries of fresh produce, dairy, fruits, vegetables, organic products, and more.

### 1.2 Key Features
- **Farm Management** — Farm profiles, farmer management, categories, organic certifications
- **Product Catalog** — Categorized products with pricing, inventory, and quality tracking
- **Subscription Management** — Weekly/monthly/custom plans with recurring deliveries
- **Order Management** — One-time orders, shopping cart, order tracking
- **Delivery & Logistics** — Zones, routes, agents, OTP verification, route optimization
- **Payments** — UPI, QR Code, Card, COD, Wallet with automated billing
- **Quality & Compliance** — Inspections, certifications, product traceability
- **Customer Engagement** — Reviews, ratings, wishlist, customer wallet

### 1.3 Technology Stack
| Component | Technology |
|---|---|
| Backend Framework | Frappe Framework v15+ |
| ERP Platform | ERPNext v15+ |
| Programming Language | Python 3.10+ |
| Database | MariaDB (Frappe default) |
| Frontend | Frappe Desk (Vue-based), Custom JS |
| CSS | Custom (`public/css/farm2home.css`) |

### 1.4 Architecture Diagram (Conceptual)
```
┌─────────────────────────────────────────────────────────────┐
│                    Farm2Home Application                      │
├─────────────────────────────────────────────────────────────┤
│   Modules:                                                   │
│   ┌──────┐ ┌────────┐ ┌──────────────┐ ┌───────────┐      │
│   │ Farm │ │Product │ │  Subscription │ │  Order    │      │
│   │ Mgmt │ │Catalog │ │  Management   │ │ Management│      │
│   └──┬───┘ └───┬────┘ └──────┬───────┘ └─────┬─────┘      │
│      │         │             │               │             │
│   ┌──▼─────────▼─────────────▼───────────────▼─────┐      │
│   │          Delivery & Logistics                    │      │
│   └──────────────────────────────────────────────────┘      │
│   ┌──────────┐  ┌────────────────────┐  ┌───────────┐      │
│   │ Payments │  │ Quality & Compliance│  │Customer   │      │
│   │          │  │                    │  │Management │      │
│   └──────────┘  └────────────────────┘  └───────────┘      │
├─────────────────────────────────────────────────────────────┤
│                    Frappe Framework v15+                      │
├─────────────────────────────────────────────────────────────┤
│                    ERPNext v15+ (Standard)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. MODULES & ARCHITECTURE

### 2.1 Module Definitions
The app defines **10 custom modules** via `farm2home/fixtures/module_def.json`:

| # | Module Name | Description |
|---|---|---|
| 1 | Farm Management | Farms, farmers, categories, certifications |
| 2 | Product Catalog | Products, categories, inventory |
| 3 | Subscription Management | Plans, subscriptions, billing |
| 4 | Customer Management | Customers, wallets, reviews, wishlists |
| 5 | Order Management | One-time and subscription orders |
| 6 | Delivery and Logistics | Zones, agents, routes, schedules |
| 7 | Payments | Transactions, refunds, wallet |
| 8 | Quality and Compliance | Inspections, certifications, quality grades |
| 9 | Configuration | Global settings, commission, delivery config |
| 10 | Farm to Home | Primary workspace, dashboards, charts |

### 2.2 Application Structure (File Tree)
```
farm2home/                           # App root (pip-installable)
├── __init__.py                      # Version = "1.0.0"
├── hooks.py                         # App hooks (hooks.py at root = legacy)
├── modules.txt                      # Module registration
├── patches.txt                      # Patch execution sequence
├── setup.py                         # Python package setup
├── requirements.txt                 # App dependencies
├── README.md                        # Project documentation
├── api.py                           # REST API whitelisted methods
├── utils.py                         # Shared utility functions (placeholder)
├── api.py                           # Marketplace API endpoints
│
├── fixtures/                        # Standard fixtures
│   ├── module_def.json              # 10 Module Def records
│   ├── role.json                    # 5 Custom roles
│   ├── workflow.json                # Subscription + Order workflows
│   ├── workflow_state.json           # 12 Workflow states
│   └── workflow_action_master.json  # 8 Workflow actions
│
├── patches/
│   └── v1_0_0/
│       ├── create_default_farm_categories.py
│       ├── create_default_product_categories.py
│       ├── create_default_subscription_plans.py
│       ├── create_default_delivery_zones.py
│       └── create_default_roles_and_permissions.py
│
├── farm_to_home/                    # Main module directory
│   ├── __init__.py
│   ├── utils.py                     # Shared helpers
│   ├── demo_data.py                 # Demo data generator
│   │
│   ├── workspace/farm_to_home/      # Workspace definition
│   │   └── farm_to_home.json        # Full workspace with shortcuts/charts
│   │
│   ├── web_form/subscription_signup/
│   │   └── subscription_signup.json # Public subscription signup form
│   │
│   ├── dashboard_chart/
│   │   ├── farm2home_monthly_sales/
│   │   ├── farm2home_subscription_growth/
│   │   └── farm2home_top_products/
│   │
│   ├── number_card/
│   │   ├── farm2home_total_orders/
│   │   ├── farm2home_active_subscriptions/
│   │   ├── farm2home_total_revenue/
│   │   └── farm2home_pending_deliveries/
│   │
│   ├── print_format/farm2home_order/
│   │   └── farm2home_order.json     # Custom order invoice print format
│   │
│   ├── notification/
│   │   ├── order_confirmation/       # Email notification on Order Submit
│   │   └── delivery_scheduled/       # Email notification on Delivery Schedule creation
│   │
│   ├── report/
│   │   ├── sales_analysis_report/
│   │   ├── subscription_revenue_report/
│   │   ├── farm_performance_report/
│   │   └── delivery_performance_report/
│   │
│   └── doctype/                     # 25+ custom DocTypes
│       ├── farm/
│       ├── farmer/
│       ├── farm_category/
│       ├── organic_certification/
│       ├── farm_certification/      [Child Table]
│       ├── farm_farmer/              [Child Table]
│       ├── farmer_farm/             [Child Table]
│       ├── farm_product/
│       ├── product/
│       ├── product_category/
│       ├── product_inventory/
│       ├── subscription_plan/
│       ├── subscription_plan_product/ [Child Table]
│       ├── subscription/
│       ├── subscription_product/     [Child Table]
│       ├── subscription_billing/
│       ├── order/
│       ├── order_item/              [Child Table]
│       ├── delivery_schedule/
│       ├── delivery_item/           [Child Table]
│       ├── delivery_agent/
│       ├── delivery_agent_zone/     [Child Table]
│       ├── delivery_zone/
│       ├── delivery_route/
│       ├── route_delivery/          [Child Table]
│       ├── payment_transaction/
│       ├── customer_wallet/
│       ├── wallet_transaction/      [Child Table]
│       ├── customer_review/
│       ├── wishlist/
│       ├── wishlist_item/           [Child Table]
│       ├── quality_inspection/
│       └── farm_to_home_settings/
│
└── public/css/
    └── farm2home.css                # Custom stylesheet
```

---

## 3. ROLES & PERMISSIONS

### 3.1 Custom Roles
Defined in `fixtures/role.json` and exported via hooks:

| Role | Desk Access | Purpose |
|---|---|---|
| **Farm Manager** | Yes | Full access to farms, products, orders, deliveries, payments |
| **Delivery Agent** | Yes | Read/write access to delivery schedules assigned to them |
| **Subscription Manager** | Yes | Manage subscription plans, subscriptions, billing |
| **Quality Inspector** | Yes | Create and manage quality inspections |
| **Farm Admin** | Yes | Manage specific farms, products (no delete rights) |
| **Customer** | No* | Web portal access: view products, create orders, manage subscriptions |

*Customer role has desk_access=0 by default but is given selective read/write on Orders, Subscriptions, Reviews, and Wishlists.

### 3.2 Standard ERPNext Roles Used
- **System Manager** — Full administrative access to all DocTypes
- **Customer** — Used for customer-facing operations (linked to Customer doctype)

### 3.3 Permission Summary by DocType

| DocType | System Manager | Farm Manager | Subscription Manager | Customer | Notes |
|---|---|---|---|---|---|
| Farm | CRUD | CRUD | — | R | — |
| Farmer | CRUD | CRUD | — | — | — |
| Farm Category | CRUD | CRU | — | — | No delete for Farm Manager |
| Product | CRUD | CRUD | — | R | — |
| Product Category | CRUD | CRU | — | — | — |
| Subscription Plan | CRUD | — | CRUD | R | — |
| Subscription | CRUD | — | CRUD | CRU | Customer can create their own |
| Order | CRUD | CRUD | — | CRU | Customer can create their own |
| Delivery Schedule | CRUD | CRUD | — | — | Delivery Agent: CRU |
| Delivery Agent | CRUD | CRU | — | — | — |
| Delivery Zone | CRUD | CRU | — | — | — |
| Payment Transaction | CRUD | CRU | — | — | — |
| Quality Inspection | CRUD | CRU | — | — | Quality Inspector: CRU |
| Customer Review | CRUD | — | — | CRU | — |
| Customer Wallet | CRUD | CRU | — | R | — |
| Wishlist | CRUD | — | — | CRU | — |
| Farm to Home Settings | CRUD | — | — | — | System Manager only |

---

## 4. DOCTYPES & DATA DICTIONARY

### 4.1 Master Data DocTypes

#### 4.1.1 Farm (`farm_to_home/doctype/farm/`)
- **Naming:** `FARM-{farm_code}-{###}`
- **Submittable:** No
- **Key Fields:**
  - `farm_name` (Data, reqd) — Display name
  - `farm_code` (Data, reqd, unique) — Short code (auto-uppercased)
  - `farm_category` (Link → Farm Category)
  - `status` (Select: Active/Inactive/Suspended)
  - `is_organic` (Check) — Organic certification flag
  - `city`, `state`, `pincode`, `country` — Location fields
  - `contact_person`, `phone`, `email` — Contact info
  - `farmers` (Table → Farm Farmer) — Associated farmers
  - `organic_certifications` (Table → Farm Certification)
  - `description` (Text Editor)
  - `images` (Attach Image)
  - **Performance Metrics (read-only):** `total_products`, `total_orders`, `total_revenue`, `customer_rating`
- **Validation:** farm_code is uppercased; `last_updated` set on each save; performance metrics recalculated on update
- **Client JS:** Custom buttons to view Products, Orders, and Update Metrics
- **Related DocTypes:** Farm Product (linked via `farm`), Order (linked via `farm`)

#### 4.1.2 Farmer (`farm_to_home/doctype/farmer/`)
- **Naming:** `FMR-{first_name}-{###}`
- **Key Fields:** `first_name`, `last_name`, `full_name` (auto-generated), `phone`, `email`, `status`, `experience_years`, `specialization`, identity & bank details
- **Child Table:** `associated_farms` (Table → Farmer Farm) — links farmers to farms with role & since_date
- **Validation:** Phone min 10 digits; full name auto-concat

#### 4.1.3 Farm Category (`farm_to_home/doctype/farm_category/`)
- **Naming:** By `category_name` (unique)
- **Fields:** `category_name`, `description`, `is_active`

#### 4.1.4 Organic Certification (`farm_to_home/doctype/organic_certification/`)
- **Naming:** By `certification_name` (unique)
- **Fields:** `certification_name`, `certifying_body`, `description`, `is_active`
- **Examples:** India Organic (NPOP), USDA Organic, EU Organic, Fair Trade Certified

#### 4.1.5 Product (`farm_to_home/doctype/product/`)
- **Naming:** `PROD-{product_code}-{###}`
- **Is Submittable:** No
- **Key Fields:**
  - `product_name` (Data, reqd), `product_code` (Data, reqd, unique)
  - `category` (Link → Product Category, reqd)
  - `product_type` (Select: Vegetable/Fruit/Dairy/Grain/Pulse/Spice/Herb/Other)
  - `is_organic` (Check)
  - `base_price`, `selling_price`, `discount_percentage`, `mrp`
  - `unit` (Select: Kg/Gram/Litre/Ml/Piece/Dozen/Bunch/Box/Packet)
  - `stock_quantity`, `reorder_level`, `warehouse`
  - `available_for_subscription`, `available_for_one_time` (Check)
  - `quality_grade`, `shelf_life_days`, `storage_instructions`
  - `product_image` (Attach Image)
- **Validation:** Selling price auto-calculated from base_price and discount; auto-mark "Out of Stock" when stock ≤ reorder_level

#### 4.1.6 Product Category (`farm_to_home/doctype/product_category/`)
- **Naming:** By `category_name` (unique)
- **Fields:** `category_name`, `parent_category` (Link → self), `category_type`, `description`, `is_active`
- **Note:** Supports hierarchical categorization

#### 4.1.7 Farm Product (`farm_to_home/doctype/farm_product/`)
- **Naming:** `FP-{farm}-{product_code}-{###}`
- **Purpose:** Links a Product to a specific Farm with farm-specific pricing
- **Key Fields:** `farm`, `product`, `product_name`, `product_code`, `status`, `season`, `is_organic`, `farmer_price`, `selling_price`, `platform_commission`, `unit`, `quantity_available`, `harvest_date`, `quality_grade`
- **Validation:** `selling_price` = `farmer_price + (farmer_price * platform_commission%)`

#### 4.1.8 Product Inventory (`farm_to_home/doctype/product_inventory/`)
- **Naming:** `INV-{product}-{####}`
- **Fields:** `product`, `warehouse`, `quantity`, `reserved_quantity`, `available_quantity` (read-only), `batch_number`, `expiry_date`, `manufacturing_date`, `status`
- **Validation:** `available_quantity = quantity - reserved_quantity`

#### 4.1.9 Delivery Zone (`farm_to_home/doctype/delivery_zone/`)
- **Naming:** By `zone_name` (unique)
- **Fields:** `zone_name`, `city`, `state`, `pincode_start`, `pincode_end`, `delivery_charge`, `minimum_order_amount`, `is_active`
- **Purpose:** Defines geographical delivery zones with pincode ranges

#### 4.1.10 Delivery Agent (`farm_to_home/doctype/delivery_agent/`)
- **Naming:** `AGT-{first_name}-{###}`
- **Fields:** `first_name`, `last_name`, `agent_name` (auto), `status`, `phone`, `email`, `vehicle_type`, `vehicle_number`, `license_number`, `license_expiry`
- **Child Table:** `assigned_zones` (Table → Delivery Agent Zone) — zone assignments with priority

#### 4.1.11 Delivery Route (`farm_to_home/doctype/delivery_route/`)
- **Naming:** `RT-{route_name}-{###}`
- **Fields:** `route_name`, `delivery_zone`, `delivery_agent`, `status`, `route_date`, `vehicle_number`, `total_stops` (read-only, auto), `estimated_distance_km`, `estimated_duration_min`, `actual_distance_km`
- **Child Table:** `route_deliveries` (Table → Route Delivery) — sequenced delivery stops

### 4.2 Transactional DocTypes

#### 4.2.1 Subscription Plan (`farm_to_home/doctype/subscription_plan/`)
- **Naming:** `SP-{plan_name}-{###}`
- **Fields:** `plan_name`, `plan_code` (unique), `plan_type` (Weekly/Monthly/Custom), `status`, `is_active`, `base_price`, `discount_amount`, `final_price` (read-only, auto), `billing_frequency`, `delivery_frequency`, `description`, `terms_and_conditions`
- **Child Table:** `subscription_products` (Table → Subscription Plan Product)
- **Validation:** `final_price = base_price - discount_amount`

#### 4.2.2 Subscription (`farm_to_home/doctype/subscription/`)
- **Naming:** `SUB-{customer}-{####}`
- **Is Submittable:** Yes
- **Workflow:** Subscription Workflow (Draft → Active → Paused/Cancelled)
- **Key Fields:** `customer`, `subscription_plan`, `plan_name`, `status`, `start_date`, `end_date`, `farm`, `delivery_address`, `delivery_zone`, `delivery_time_slot`, `delivery_day`, `billing_frequency`, `subscription_amount`, `discount_applied`, `total_amount`, `paid_amount`, `balance_amount`, `payment_mode`, `is_paused`, `pause_start_date`, `pause_end_date`, `next_delivery_date` (auto), `last_delivery_date` (auto), `total_deliveries` (auto), `total_payments` (auto)
- **Child Table:** `subscription_products` (Table → Subscription Product)
- **Lifecycle:**
  1. **Draft** → Submit → **Active** (via `on_submit`)
  2. **Active** → Pause → **Paused** (via custom button/client JS)
  3. **Paused** → Resume → **Active**
  4. **Active** → Cancel → **Cancelled** (via `on_cancel`)
  5. **Expired** — reached end_date
- **Client JS Functions:** Pause/Resume custom buttons; auto-populate plan pricing

#### 4.2.3 Subscription Billing (`farm_to_home/doctype/subscription_billing/`)
- **Naming:** `BILL-{subscription}-{####}`
- **Fields:** `subscription`, `customer`, `status`, `billing_period_start`, `billing_period_end`, `subscription_amount`, `additional_charges`, `discount`, `total_amount` (read-only), `paid_amount`, `balance_amount`, `payment_status`, `invoice_number`, `due_date`
- **Validation:** `total_amount = subscription_amount + additional_charges - discount`; `balance_amount = total_amount - paid_amount`
- **Scheduled Task:** `generate_monthly_bills()` runs daily to create bills for active subscriptions

#### 4.2.4 Order (`farm_to_home/doctype/order/`)
- **Naming:** `ORD-{customer}-{####}`
- **Is Submittable:** Yes
- **Workflow:** Order Workflow (Draft → Confirmed → Out for Delivery → Delivered/Cancelled)
- **Key Fields:** `customer`, `customer_name`, `order_type` (One-time/Subscription), `status`, `order_date`, `delivery_date`, `farm`, `farm_name`, `subtotal` (read-only), `tax_amount`, `delivery_charge`, `discount_amount`, `grand_total` (read-only), `paid_amount`, `balance_amount` (read-only), `delivery_address`, `delivery_zone`, `delivery_time_slot`, `delivery_agent`, `tracking_number`, `payment_mode`, `payment_status`, `customer_notes`, `internal_notes`
- **Child Table:** `order_items` (Table → Order Item)
- **Lifecycle:**
  1. **Draft** → Submit → **Confirmed** (via `on_submit`)
  2. **Confirmed** → **Out for Delivery** → **Delivered** (status sync from Delivery Schedule)
  3. **Cancelled** (via `on_cancel`)
- **Server-side Logic:**
  - `on_submit`: Creates Delivery Schedule, deducts inventory
  - `on_cancel`: Restores inventory, cancels future deliveries
  - `update_order_status()` (hourly): Syncs Order status from linked Deliveries

#### 4.2.5 Delivery Schedule (`farm_to_home/doctype/delivery_schedule/`)
- **Naming:** `DEL-{customer}-{####}`
- **Fields:** `customer`, `order`, `subscription`, `status` (Scheduled/Confirmed/Out for Delivery/Delivered/Cancelled/Failed/Returned), `delivery_date`, `delivery_time_slot`, `delivery_zone`, `delivery_route`, `delivery_agent`, `agent_name`, `vehicle_number`, `delivery_address`, `address_display`, `tracking_number`, `otp_verification`, `delivery_otp`, `actual_delivery_time`, `delivery_confirmation`, `customer_signature`, `delivery_photo`, `delivery_notes`, `customer_feedback`
- **Child Table:** `delivery_items` (Table → Delivery Item) — item-level tracking with delivered_quantity & status
- **Lifecycle:** Scheduled → Confirmed → Out for Delivery → Delivered

#### 4.2.6 Payment Transaction (`farm_to_home/doctype/payment_transaction/`)
- **Naming:** `PAY-{customer}-{####}`
- **Is Submittable:** Yes
- **Fields:** `customer`, `order`, `subscription`, `status`, `payment_date`, `payment_mode`, `amount`, `transaction_fee`, `total_amount` (read-only), `currency`, `transaction_id`, `reference_number`, `gateway_response`, `upi_id`, `qr_code_reference`, `is_refunded`, `refund_amount`, `refund_date`, `refund_reason`
- **Server-side Logic:**
  - `on_submit`: Updates Order payment_status, Subscription paid_amount, and Wallet balance

#### 4.2.7 Customer Wallet (`farm_to_home/doctype/customer_wallet/`)
- **Naming:** `WAL-{customer}`
- **Fields:** `customer` (unique), `customer_name`, `balance`, `total_credited`, `total_debited` (all read-only except balance)
- **Child Table:** `transactions` (Table → Wallet Transaction)
- **Validation:** Auto-calculates totals and balance from child transactions

#### 4.2.8 Customer Review (`farm_to_home/doctype/customer_review/`)
- **Naming:** `REV-{customer}-{####}`
- **Fields:** `customer`, `customer_name`, `farm`, `product`, `rating` (Rating field, reqd), `review_date`, `order`, `review_title`, `review_text`, `is_approved`, `is_featured`
- **Server-side Logic:** `on_update` recalculates Farm rating and Product rating averages

#### 4.2.9 Wishlist (`farm_to_home/doctype/wishlist/`)
- **Naming:** `WIS-{customer}-{####}`
- **Fields:** `customer` (unique), `customer_name`
- **Child Table:** `wishlist_items` (Table → Wishlist Item)

#### 4.2.10 Quality Inspection (`farm_to_home/doctype/quality_inspection/`)
- **Naming:** `QI-{product}-{####}`
- **Fields:** `product`, `product_name`, `farm`, `farm_name`, `status` (Draft/Inspected/Approved/Rejected), `inspection_date`, `inspector`, `appearance`, `freshness`, `size_uniformity` (Rating fields), `pesticide_residue`, `moisture_content`, `overall_grade`, `organic_verified`, `certification_number`, `lab_test_report`, `test_date`, `result` (Pass/Fail/Conditional), `remarks`
- **Server-side Logic:** `on_submit` sets status based on result, updates Product quality_grade

#### 4.2.11 Farm to Home Settings (`farm_to_home/doctype/farm_to_home_settings/`)
- **Naming:** By `settings_name` (unique)
- **Fields:**
  - **General:** `platform_name`, `default_currency`, `enable_subscriptions`, `enable_wallet`
  - **Commission:** `default_commission_percentage` (default 10%), `minimum_commission_amount`
  - **Delivery:** `default_delivery_charge` (default 30), `free_delivery_threshold` (default 500), `enable_otp_verification`, `enable_route_optimization`
  - **Notification:** `order_confirmation_template`, `delivery_notification_template`, `payment_confirmation_template` (Email Template links)

### 4.3 Child Table DocTypes

| Child Table | Parent DocType | Purpose |
|---|---|---|
| Farm Farmer | Farm | Links farmers to farms with role (Owner/Manager/Worker/Partner) |
| Farmer Farm | Farmer | Links farms to farmers with role and since_date |
| Farm Certification | Farm | Organic certification records with number, dates, attachment |
| Subscription Plan Product | Subscription Plan | Products included in a plan with quantity & price |
| Subscription Product | Subscription | Products included in a customer's subscription |
| Order Item | Order | Individual line items with product, qty, rate, amount |
| Delivery Item | Delivery Schedule | Item-level tracking with delivered qty & status |
| Delivery Agent Zone | Delivery Agent | Zone assignments with priority |
| Route Delivery | Delivery Route | Sequenced stops on a delivery route |
| Wallet Transaction | Customer Wallet | Credit/debit entries with reference & date |
| Wishlist Item | Wishlist | Saved products with added date & notes |

---

## 5. WORKFLOWS

### 5.1 Workflow States Registry
Defined in `fixtures/workflow_state.json` — 12 states registered:
`Draft`, `Active`, `Paused`, `Cancelled`, `Confirmed`, `Out for Delivery`, `Delivered`, `Pending`, `Returned`, `Inspected`, `Approved`, `Rejected`

### 5.2 Workflow Actions Registry
Defined in `fixtures/workflow_action_master.json` — 8 actions:
`Approve`, `Reject`, `Cancel`, `Resume`, `Pause`, `Confirm`, `Deliver`, `Return`

### 5.3 Subscription Workflow
**Document Type:** Subscription  
**State Field:** `status`  
**States & Transitions:**

```
        ┌─────────┐
        │  Draft  │
        └────┬────┘
             │ Approve
             ▼
        ┌─────────┐          ┌─────────┐
        │ Active  │◄─────────│ Paused  │
        └────┬────┘  Resume  └─────────┘
         │   │                    ▲
    Pause│   │Cancel              │
         │   ▼                    │
         │ ┌──────────┐           │
         │ │ Cancelled│           │
         │ └──────────┘           │
         └────────────────────────┘
```

- **Draft → Active:** Approve (allowed: System Manager)
- **Active → Paused:** Pause (allowed: System Manager)
- **Paused → Active:** Resume (allowed: System Manager)
- **Active → Cancelled:** Cancel (allowed: System Manager)

### 5.4 Order Workflow
**Document Type:** Order  
**State Field:** `status`  
**States & Transitions:**

```
        ┌─────────┐
        │  Draft  │
        └────┬────┘
             │ Confirm
             ▼
       ┌─────────────┐
       │  Confirmed   │
       └──────┬───────┘
          Deliver│   │Cancel
                ▼   ▼
     ┌─────────────────┐   ┌──────────┐
     │Out for Delivery │   │ Cancelled│
     └────────┬────────┘   └──────────┘
              │ Deliver
              ▼
        ┌───────────┐
        │ Delivered │
        └───────────┘
```

- **Draft → Confirmed:** Confirm (allowed: System Manager)
- **Confirmed → Out for Delivery:** Deliver (allowed: System Manager)
- **Out for Delivery → Delivered:** Deliver (allowed: System Manager)
- **Confirmed → Cancelled:** Cancel (allowed: System Manager)

---

## 6. AUTOMATED SCHEDULED TASKS

Defined in `hooks.py` under `scheduler_events`:

### 6.1 Daily Tasks (runs once per day)

| Task | Method | Description |
|---|---|---|
| Process Daily Subscriptions | `subscription.subscription.process_daily_subscriptions` | Finds active subscriptions with `next_delivery_date = today`, creates Delivery Schedules, updates next delivery date |
| Generate Daily Delivery Schedules | `delivery_schedule.delivery_schedule.generate_daily_delivery_schedules` | Creates Delivery Schedule records for active subscriptions due today |
| Generate Monthly Bills | `subscription_billing.subscription_billing.generate_monthly_bills` | Creates `Subscription Billing` records for all active subscriptions at month start |

### 6.2 Hourly Tasks

| Task | Method | Description |
|---|---|---|
| Update Order Statuses | `order.order.update_order_status` | Syncs Order status (Confirmed → Out for Delivery → Delivered) based on linked Delivery Schedule statuses |

### 6.3 Weekly Tasks

| Task | Method | Description |
|---|---|---|
| Update Farm Performance Metrics | `farm.farm.update_farm_performance_metrics` | Recalculates `total_products`, `total_orders`, `total_revenue` for all farms |

### 6.4 Cron Tasks

| Time | Task | Method |
|---|---|---|
| 6:00 AM daily | Send delivery reminders | `subscription.subscription.send_daily_reminders` — emails customers about tomorrow's delivery |
| 8:00 PM daily | Optimize routes | `delivery_schedule.delivery_schedule.optimize_routes` — groups tomorrow's deliveries by zone and assigns route names |

### 6.5 Scheduler Flow Diagram
```
Daily 6:00 AM
  └─ send_daily_reminders ──→ Email customers with deliveries tomorrow

Daily (system default time)
  ├─ process_daily_subscriptions ──→ Create deliveries for subscriptions due today
  ├─ generate_daily_delivery_schedules → Additional schedule generation
  └─ generate_monthly_bills ──→ Create Subscription Billing records

Hourly
  └─ update_order_status ──→ Sync order statuses from delivery schedules

Weekly
  └─ update_farm_performance_metrics → Recalculate farm KPIs

Daily 8:00 PM
  └─ optimize_routes ──→ Group deliveries by zone for tomorrow
```

---

## 7. DOCUMENT EVENTS (HOOKS)

Defined in `hooks.py` under `doc_events`:

| DocType | Event | Handler | Description |
|---|---|---|---|
| **Subscription** | `on_submit` | `subscription.subscription.on_submit` | Sets status = "Active", creates initial delivery schedule |
| **Subscription** | `on_cancel` | `subscription.subscription.on_cancel` | Sets status = "Cancelled", cancels future deliveries |
| **Order** | `on_submit` | `order.order.on_submit` | Sets status = "Confirmed", creates Delivery Schedule, deducts inventory |
| **Order** | `on_cancel` | `order.order.on_cancel` | Sets status = "Cancelled", restores inventory |
| **Payment Transaction** | `on_submit` | `payment_transaction.payment_transaction.on_submit` | Sets status = "Completed", updates Order payment, Subscription payment, Wallet deduction |
| **Delivery Schedule** | `on_update` | `delivery_schedule.delivery_schedule.on_update` | Generates tracking number (when Out for Delivery), records actual delivery time (when Delivered), updates linked Order & Subscription |
| **Quality Inspection** | `on_submit` | `quality_inspection.quality_inspection.on_submit` | Sets status based on result (Approved/Rejected/Inspected), updates Product quality_grade |

---

## 8. API ENDPOINTS

All endpoints are `@frappe.whitelist()` methods accessible via `/api/method/farm2home.api.*`:

### 8.1 Public Endpoints (Guest Access)

| Endpoint | Description | Returns |
|---|---|---|
| `get_marketplace_data()` | Marketplace homepage data | Featured farms, products, plans, categories |
| `get_farm_detail(farm_name)` | Detailed farm info with products & reviews | Farm doc, products list, reviews |
| `get_product_detail(product_name)` | Product details with available farms & reviews | Product doc, farms list, reviews |
| `search_products_and_farms(search_text, category, product_type, is_organic, city)` | Search across products and farms | Matching products & farms |

### 8.2 Authenticated Endpoints (Customer)

| Endpoint | Description | Parameters |
|---|---|---|
| `create_customer_order(customer, items, delivery_address, ...)` | Place a new one-time order | customer, items (array), delivery_address, delivery_zone, payment_mode, delivery_date, customer_notes |
| `create_customer_subscription(customer, subscription_plan, start_date, ...)` | Create a new subscription | customer, subscription_plan, start_date, delivery_address, delivery_time_slot, payment_mode |
| `get_customer_dashboard(customer)` | Customer dashboard data | Active subscriptions, recent orders, upcoming deliveries, wallet balance |
| `add_to_wishlist(customer, product)` | Add product to wishlist | customer, product |
| `get_delivery_tracking(tracking_number)` | Track a delivery by tracking number | tracking_number |

### 8.3 Internal Whitelisted Methods

| Endpoint | DocType | Purpose |
|---|---|---|
| `get_product_price(product)` | Product | Get selling price, MRP, discount |
| `search_products(category, product_type, is_organic, search_text)` | Product | Filter/search products |
| `get_farm_products_by_farm(farm)` | Farm Product | List products for a farm |
| `get_farmer_farms(farmer)` | Farmer | Get farms associated with a farmer |
| `get_farm_dashboard_data(farm)` | Farm | Farm-level KPIs |
| `process_refund(payment_transaction, amount, reason)` | Payment Transaction | Process a refund |
| `add_wallet_balance(customer, amount, reference)` | Customer Wallet | Credit customer wallet |
| `get_wallet_balance(customer)` | Customer Wallet | Get wallet balance |
| `pause_subscription(subscription, start_date, end_date, reason)` | Subscription | Pause a subscription |
| `resume_subscription(subscription)` | Subscription | Resume a paused subscription |
| `confirm_delivery(delivery, otp, notes)` | Delivery Schedule | Confirm delivery with OTP |
| `create_quality_inspection(product, farm)` | Quality Inspection | Create a new inspection request |

---

## 9. REPORTS & DASHBOARDS

### 9.1 Workspace
**Name:** Farm to Home  
**File:** `farm_to_home/workspace/farm_to_home/farm_to_home.json`

The workspace contains:
- **8 Shortcuts:** Farm, Product, Subscription, Order, Delivery Schedule, Payment Transaction, Customer, Quality Inspection
- **4 Number Cards:** Total Orders, Active Subscriptions, Total Revenue, Pending Deliveries
- **3 Charts:** Monthly Sales (Bar), Subscription Growth (Line), Top Products (Donut)
- **10 Link Cards** organized in sections: Farm Management, Product Management, Subscription Management, Customer Management, Order Management, Delivery & Logistics, Payments, Quality & Compliance, Reports & Analytics, Configuration

### 9.2 Dashboard Charts

| Chart | Type | Document Type | Value Field | Time Interval |
|---|---|---|---|---|
| Farm2Home Monthly Sales | Bar | Order | Sum of `grand_total` | Monthly (Last Year) |
| Farm2Home Subscription Growth | Line | Subscription | Count | Monthly (Last Year) |
| Farm2Home Top Products | Donut | Order Item | Sum of `amount` (top 10) | N/A |

### 9.3 Number Cards

| Card | Document Type | Function | Filter |
|---|---|---|---|
| Total Orders | Order | Count | docstatus = 1 |
| Active Subscriptions | Subscription | Count | status = Active, docstatus = 1 |
| Total Revenue | Order | Sum of `grand_total` | docstatus = 1 |
| Pending Deliveries | Delivery Schedule | Count | status in (Scheduled, Confirmed, Out for Delivery) |

### 9.4 Custom Reports

| Report | Module | Purpose | Key Columns |
|---|---|---|---|
| **Sales Analysis Report** | Farm to Home | Sales data grouped by date & order type | Order Date, Order Type, Total Orders, Total Revenue, Total Items |
| **Subscription Revenue Report** | Farm to Home | Revenue broken down by subscription plan | Subscription Plan, Plan Type, Total Subscriptions, Total Revenue, Active Subscriptions |
| **Farm Performance Report** | Farm to Home | Farm-level KPIs | Farm, Farm Name, Total Products, Total Orders, Total Revenue, Customer Rating |
| **Delivery Performance Report** | Farm to Home | Delivery agent performance metrics | Delivery Agent, Agent Name, Total Deliveries, Delivered, Failed, Delivery Rate |

### 9.5 Report Filters
All reports support date range filters (`from_date`, `to_date`). Additional filters:
- **Sales Analysis:** `farm`, `order_type`
- **Subscription Revenue:** `plan_type`
- **Farm Performance:** Date range
- **Delivery Performance:** Date range

---

## 10. NOTIFICATIONS

### 10.1 Order Confirmation
| Property | Value |
|---|---|
| **Channel** | Email + System Notification |
| **Document Type** | Order |
| **Event** | Submit |
| **Recipients** | Customer (via `customer` field) |
| **Subject** | "Order Confirmed - {{ doc.name }}" |
| **Attach Print** | Yes (Farm2Home Order print format) |

### 10.2 Delivery Scheduled
| Property | Value |
|---|---|
| **Channel** | Email + System Notification |
| **Document Type** | Delivery Schedule |
| **Event** | New |
| **Recipients** | Customer (via `customer` field) |
| **Subject** | "Delivery Scheduled - {{ doc.name }}" |

---

## 11. PRINT FORMATS

### 11.1 Farm2Home Order
**File:** `farm_to_home/print_format/farm2home_order/farm2home_order.json`

A custom Jinja-based print format for Orders with:
- Branded header with "Farm2Home Order" title
- Customer details, order date, delivery date, status, payment mode
- Itemized table (Product, Quantity, Unit, Rate, Amount)
- Totals section (Subtotal, Tax, Delivery Charge, Discount, Grand Total)
- Customer notes section
- Green-themed CSS styling

---

## 12. WEB FORMS

### 12.1 Subscription Signup
**Route:** `/subscription-signup`  
**File:** `farm_to_home/web_form/subscription_signup/subscription_signup.json`

- **DocType:** Subscription
- **Login Required:** Yes
- **Published:** Yes
- **Allow Multiple:** Yes
- **Allow Edit:** Yes
- **Fields:**
  1. Customer (Link → Customer, required)
  2. Subscription Plan (Link → Subscription Plan, required)
  3. Start Date (Date, required)
  4. Delivery Address (Link → Address, required)
  5. Delivery Time Slot (Select: 6 AM - 8 AM / 8 AM - 10 AM / 10 AM - 12 PM / 4 PM - 6 PM / 6 PM - 8 PM)
  6. Payment Mode (Select: UPI/Card/Cash on Delivery/Wallet, required)

---

## 13. INSTALLATION & SETUP

### 13.1 Prerequisites
- Frappe Framework v15+
- ERPNext v15+
- Python 3.10+
- Node.js 18+ (for assets)
- MariaDB 10.6+
- Redis

### 13.2 Installation Steps

```bash
# 1. Get the app
bench get-app https://github.com/farm2home/farm2home.git

# 2. Install on site
bench --site [site-name] install-app farm2home

# 3. Run migrations
bench --site [site-name] migrate

# 4. Build assets (if needed)
bench build

# 5. Set site as default (optional)
bench use [site-name]
```

### 13.3 Post-Installation Steps

1. **Set up Farm2Home Settings:**
   - Navigate: Farm to Home → Configuration → Farm2Home Settings
   - Create a new settings record (e.g., "Default Settings")
   - Configure platform name, default currency, commission %, delivery charges

2. **Assign User Roles:**
   - Set up users and assign appropriate roles:
     - `Farm Manager` for farm operators
     - `Subscription Manager` for subscription administrators
     - `Delivery Agent` for delivery personnel
     - `Quality Inspector` for quality control staff
     - `Farm Admin` for farm-level administrators

3. **Configure Fixtures:**
   - Run `bench --site [site] migrate` to load all fixtures:
     - Module definitions (10 modules)
     - Roles (5 custom roles)
     - Workflows (Subscription & Order)
     - Workflow States (12 states)
     - Workflow Actions (8 actions)

4. **Enable Scheduler:**
   ```bash
   bench --site [site] scheduler enable
   ```

5. **Create Master Data** (see section 14 for demo data):
   - Farm Categories
   - Product Categories
   - Organic Certifications
   - Delivery Zones
   - Products
   - Subscription Plans

6. **Configure Notifications:**
   - Verify Order Confirmation notification is enabled
   - Verify Delivery Scheduled notification is enabled
   - Set up email settings in Frappe for outbound mail

### 13.4 Uninstallation

```bash
bench --site [site-name] uninstall-app farm2home
bench --site [site-name] migrate
```

---

## 14. DATA GENERATION (DEMO/TEST)

### 14.1 Demo Data Script
**File:** `farm_to_home/demo_data.py`

A comprehensive demo data generator creates realistic, fully-linked data across all custom DocTypes.

### 14.2 Running the Generator

```bash
bench --site [site-name] execute farm2home.farm_to_home.demo_data.create_demo_data
```

### 14.3 Data Generated

| DocType | Quantity | Notes |
|---|---|---|
| Farm Category | 10 | Organic Farm, Vegetable Farm, Dairy Farm, etc. |
| Organic Certification | 15 | India Organic, USDA Organic, EU Organic, etc. |
| Product Category | 15 | Leafy Greens, Root Vegetables, Dairy, etc. |
| Farm | 10 | With certifications, descriptions |
| Farmer | 20 | With linked farms, bank details, identity docs |
| Delivery Zone | 10 | Covering major Indian cities |
| Delivery Agent | 20 | With zone assignments, vehicle details |
| Product | 50 | Vegetables, fruits, dairy, grains, spices |
| Farm Product | 50 | Links products to farms with farm-specific pricing |
| Product Inventory | 50 | Warehouse records with batch tracking |
| Customer | 30 | Using standard ERPNext Customer |
| Customer Address | ~50 | Linked to customers with shipping/billing types |
| Subscription Plan | 10 | Various plans with products |
| Subscription | 50 | With varying statuses (Active/Paused/Cancelled) |
| Order | 100 | With line items, delivery info, varied statuses |
| Delivery Route | 20 | With zone/agent assignments |
| Delivery Schedule | 100 | Linked to orders/subscriptions |
| Payment Transaction | 100 | UPI/Card/COD with varied statuses |
| Subscription Billing | ~60 | Monthly bills for subscriptions |
| Customer Review | 40 | Ratings and reviews for products/farms |
| Customer Wallet | 30 | With transaction history |
| Wishlist | 30 | With saved products |
| Quality Inspection | 30 | With grades and results |

### 14.4 Cleanup Demo Data

```bash
bench --site [site-name] execute farm2home.farm_to_home.demo_data.cleanup_demo_data
```

This deletes all generated data in dependency-safe order and resets autoname series counters.

### 14.5 Execution Order (Dependency-Aware)
```
Step 1: Base Reference Data (no dependencies)
  → Farm Categories → Organic Certifications → Product Categories

Step 2: Core Entities
  → Farms → Farmers → Delivery Zones → Delivery Agents

Step 3: Products & Inventory
  → Products → Farm Products → Product Inventory

Step 4: Customers
  → Customers (standard ERPNext) → Addresses

Step 5: Subscriptions
  → Subscription Plans → Subscriptions

Step 6: Orders & Deliveries
  → Orders → Delivery Routes → Delivery Schedules

Step 7: Payments & Billing
  → Payment Transactions → Subscription Billings

Step 8: Customer Engagement
  → Customer Reviews → Customer Wallets → Wishlists

Step 9: Quality
  → Quality Inspections
```

---

## 15. PATCHES & MIGRATIONS

### 15.1 Patch Registration
Patches are registered in `patches.txt` (root) and `farm2home/patches.txt`:

```
farm2home.patches.v1_0_0.create_default_farm_categories
farm2home.patches.v1_0_0.create_default_product_categories
farm2home.patches.v1_0_0.create_default_subscription_plans
farm2home.patches.v1_0_0.create_default_delivery_zones
farm2home.patches.v1_0_0.create_default_roles_and_permissions
farm2home.patches.v1_0_0.cleanup_event_customer_field
```

### 15.2 Available Patches

| Patch | Purpose |
|---|---|
| `create_default_farm_categories` | Creates 10 default farm categories |
| `create_default_product_categories` | Creates default product categories |
| `create_default_subscription_plans` | Creates 10 subscription plans with products |
| `create_default_delivery_zones` | Creates 10 delivery zones for major cities |
| `create_default_roles_and_permissions` | Sets up custom roles and DocType permissions |
| `cleanup_event_customer_field` | Cleanup patch for stray Event-Customer custom field references |

### 15.3 Running Patches Manually

```bash
# Run all pending patches
bench --site [site] migrate

# Run a specific patch
bench --site [site] execute farm2home.patches.v1_0_0.[patch_name]
```

---

## 16. BACKUP & RESTORE

### 16.1 Backup

```bash
# Full backup (site + files)
bench --site [site-name] backup

# Backup with specific backup path
bench --site [site-name] backup --backup-path /path/to/backups

# Partial backup (database only)
bench --site [site-name] backup --with-files
```

### 16.2 Restore

```bash
# Restore from backup
bench --site [site-name] restore /path/to/backup.sql.gz
```

### 16.3 Backup Key Data Before Major Changes
Always backup before:
- Running patches
- Upgrading the app
- Running demo data scripts that may modify production data
- Deleting large volumes of data

---

## 17. TROUBLESHOOTING

### 17.1 Common Issues

| Issue | Likely Cause | Solution |
|---|---|---|
| Workflow actions not appearing | Workflow states/actions missing | Run `bench --site [site] migrate` to load fixtures |
| Demo data creation failures | Missing dependencies | Execute steps in correct order (see §14.5) |
| Notifications not sending | Email settings not configured | Configure Email Domain & Email Account in Frappe |
| Subscription auto-renewals not firing | Scheduler disabled | `bench --site [site] scheduler enable` |
| Order/Delivery status not syncing | Hourly job not running | Check scheduler logs: `bench --site [site] scheduler log` |
| Permission errors | Roles not assigned | Assign roles in Frappe User document |
| "ModuleNotFoundError" for notifications | Empty `__init__.py` missing in notification directory | Ensure each notification has an `__init__.py` file |
| Print format not rendering | Template syntax error | Check Jinja template in print format HTML |
| Custom CSS not loading | Assets not built | Run `bench build` |

### 17.2 Debugging Commands

```bash
# View scheduler logs
bench --site [site] scheduler log

# Run a specific scheduled task manually
bench --site [site] execute farm2home.farm_to_home.doctype.subscription.subscription.process_daily_subscriptions

# Clear cache
bench --site [site] clear-cache

# Check pending patches
bench --site [site] list-pending-patches

# View recent error logs
bench --site [site] console

# Rebuild all assets
bench build --app farm2home

# Check DocType status
bench --site [site] set-doctype-status --all
```

### 17.3 Logs Location
- Frappe error logs: `./logs/error.log`
- Scheduler logs: `./logs/scheduler.log`
- Database queries: `./logs/query.log` (when enabled)

---

## 18. APPENDIX

### 18.1 File Index

| File Path | Purpose |
|---|---|
| `hooks.py` | App configuration, doc_events, scheduler events, fixtures |
| `modules.txt` | Module registration for Frappe |
| `patches.txt` | Sequence of data migration patches |
| `setup.py` | Python package definition |
| `requirements.txt` | Python dependencies (frappe) |
| `api.py` | Public REST API endpoints |
| `farm_to_home/utils.py` | Shared utility functions (settings, dashboard, search) |
| `farm_to_home/demo_data.py` | Demo data generator and cleanup |
| `farm_to_home/fixtures/*.json` | Fixture exports (roles, workflows, states) |

### 18.2 Key Business Flows

#### A. Customer Subscription Flow
```
Customer discovers plan → Web Form Signup
  → Creates Subscription in Draft
  → Submit triggers on_submit
    → Status becomes Active
    → Initial delivery schedule created
  → Daily scheduler (process_daily_subscriptions)
    → Creates Delivery Schedule for today's deliveries
  → Customer receives email notification
  → Delivery agent assigned to route
  → Delivery confirmed with OTP
```

#### B. Customer One-Time Order Flow
```
Customer browses products → API: create_customer_order
  → Creates Order in Draft
  → Submit triggers on_submit
    → Status becomes Confirmed
    → Delivery Schedule created
    → Inventory deducted
  → Hourly scheduler updates order status
  → Delivery completed → Status = Delivered
```

#### C. Payment & Wallet Flow
```
Customer pays → Payment Transaction created
  → Submit triggers on_submit
    → Status = Completed
    → Order payment_status updated
    → Subscription paid_amount updated
    → Wallet debited (if payment_mode = Wallet)
  → Optional: Refund via process_refund API
```

#### D. Quality Inspection Flow
```
Manager creates inspection → Quality Inspection created (Draft)
  → Inspector fills quality parameters
  → Submit triggers on_submit
    → Status = Approved/Rejected based on result
    → Product quality_grade updated
```

### 18.3 Delivery Schedule On-Update Logic
When a Delivery Schedule is updated:
1. If status changes to "Out for Delivery" and no tracking number exists → auto-generates tracking number
2. If status changes to "Delivered" and no actual delivery time → records current time
3. Linked Order status synced (if Order exists and delivery is Delivered)
4. Linked Subscription `last_delivery_date` updated (if Subscription exists)

### 18.4 Route Optimization Logic
The `optimize_routes()` function (runs nightly at 8 PM):
1. Fetches all Scheduled deliveries for tomorrow
2. Groups them by `delivery_zone`
3. Assigns a route name (`ROUTE-{zone}-{date}`) to each delivery in the group
4. This enables delivery agents to see their grouped deliveries for the day

### 18.5 Delivery OTP Verification
- Each Delivery Schedule gets a random 4-character OTP on creation (via `random_string(4).upper()`)
- `confirm_delivery()` API endpoint validates the OTP before marking as Delivered
- Configurable via `enable_otp_verification` in Farm2Home Settings

### 18.6 Stateful DocTypes at a Glance

| DocType | States | State Machine |
|---|---|---|
| Subscription | Draft → Active → Paused/Cancelled/Expired | Workflow + Code |
| Order | Draft → Confirmed → Out for Delivery → Delivered/Cancelled | Workflow + Code |
| Delivery Schedule | Scheduled → Confirmed → Out for Delivery → Delivered/Cancelled/Failed/Returned | Code only |
| Payment Transaction | Pending → Completed/Failed/Refunded/Cancelled | Code + User |
| Quality Inspection | Draft → Inspected → Approved/Rejected | Code + User |

---

**END OF DOCUMENT**

---

*This SOP is maintained as part of the Farm2Home application documentation. For questions or updates, contact the Farm2Home Team at support@farm2home.local.*
