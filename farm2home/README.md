# Farm to Home Subscription Platform

A comprehensive Farm-to-Home Subscription Platform built for ERPNext v15+ and Frappe Framework v15+.

## Overview

Farm2Home connects farmers directly with customers through a subscription-based marketplace. The platform supports recurring deliveries, fresh produce, dairy products, fruits, vegetables, organic products, and doorstep delivery services.

## Features

### Farm Management
- Farm profiles and farmer management
- Farm categories and organic certifications
- Farm products and seasonal products
- Crop management and harvest planning

### Product Catalog
- Product categories and variants
- Product pricing and inventory
- Product batches and quality grades

### Subscription Management
- Weekly, monthly, and custom subscription plans
- Subscription deliveries and renewals
- Pause, modify, and cancel subscriptions

### Order Management
- Shopping cart and one-time orders
- Order tracking and status management
- Order history

### Delivery & Logistics
- Delivery routes and zones
- Delivery schedules and agents
- Route optimization and tracking
- OTP verification

### Payments
- UPI, QR Code, Card, Cash on Delivery
- Payment transactions and refunds
- Subscription billing
- Customer wallet

### Quality & Compliance
- Quality inspections
- Product certifications
- Organic verification
- Product traceability

### Marketplace
- Farm listings and product listings
- Customer reviews and ratings
- Wishlist and featured products

## Installation

1. Get the app:
```bash
bench get-app https://github.com/farm2home/farm2home.git
```

2. Install on your site:
```bash
bench --site [site-name] install-app farm2home
```

3. Migrate:
```bash
bench --site [site-name] migrate
```

## Requirements

- Frappe Framework v15+
- ERPNext v15+
- Python 3.10+

## Modules

- Farm Management
- Product Catalog
- Subscription Management
- Customer Management
- Order Management
- Delivery and Logistics
- Payments
- Quality and Compliance
- Marketplace
- Reports
- Configuration

## License

MIT
