import frappe
from frappe.utils import today, add_days

def get_default_farm2home_settings():
    settings = frappe.get_doc("Farm to Home Settings", {"is_active": 1})
    if not settings:
        settings = frappe.get_doc("Farm to Home Settings")
    return settings

def get_customer_active_subscriptions(customer):
    return frappe.get_all("Subscription",
        filters={
            "customer": customer,
            "status": "Active",
            "docstatus": 1
        },
        fields=["name", "subscription_plan", "plan_name", "next_delivery_date", "total_amount"]
    )

def get_customer_pending_orders(customer):
    return frappe.get_all("Order",
        filters={
            "customer": customer,
            "status": ["in", ["Draft", "Confirmed", "Processing", "Out for Delivery"]],
            "docstatus": 1
        },
        fields=["name", "order_date", "status", "grand_total", "delivery_date"]
    )

def get_customer_wallet_balance(customer):
    wallet = frappe.get_doc("Customer Wallet", {"customer": customer})
    return wallet.balance if wallet else 0

def get_delivery_zones_for_pincode(pincode):
    zones = frappe.get_all("Delivery Zone",
        filters={
            "is_active": 1,
            "pincode_start": ["<=", pincode],
            "pincode_end": [">=", pincode]
        },
        fields=["name", "zone_name", "delivery_charge", "minimum_order_amount"]
    )
    return zones

def get_featured_farms(limit=6):
    return frappe.get_all("Farm",
        filters={"status": "Active"},
        fields=["name", "farm_name", "farm_rating", "is_organic", "images"],
        order_by="farm_rating desc",
        limit=limit
    )

def get_featured_products(limit=8):
    return frappe.get_all("Product",
        filters={"status": "Active", "available_for_one_time": 1},
        fields=["name", "product_name", "selling_price", "unit", "product_image", "is_organic"],
        order_by="modified desc",
        limit=limit
    )

def get_subscription_plans():
    return frappe.get_all("Subscription Plan",
        filters={"is_active": 1, "status": "Active"},
        fields=["name", "plan_name", "plan_type", "final_price", "billing_frequency", "description"]
    )

def generate_otp():
    import random
    return str(random.randint(1000, 9999))

def send_sms_notification(phone, message):
    # Integrate with SMS gateway
    frappe.log_error(f"SMS to {phone}: {message}", "Farm2Home SMS")

def get_dashboard_stats():
    return {
        "total_farms": frappe.db.count("Farm", {"status": "Active"}),
        "total_products": frappe.db.count("Product", {"status": "Active"}),
        "total_customers": frappe.db.count("Customer"),
        "active_subscriptions": frappe.db.count("Subscription", {"status": "Active", "docstatus": 1}),
        "today_orders": frappe.db.count("Order", {"order_date": today(), "docstatus": 1}),
        "pending_deliveries": frappe.db.count("Delivery Schedule", {"status": ["in", ["Scheduled", "Confirmed", "Out for Delivery"]]})
    }
