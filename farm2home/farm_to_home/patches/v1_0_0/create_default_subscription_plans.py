import frappe

def execute():
    plans = [
        {
            "plan_name": "Weekly Veggie Box",
            "plan_code": "WVB-001",
            "plan_type": "Weekly",
            "base_price": 499,
            "billing_frequency": "Weekly",
            "delivery_frequency": "Weekly"
        },
        {
            "plan_name": "Monthly Organic Basket",
            "plan_code": "MOB-001",
            "plan_type": "Monthly",
            "base_price": 1999,
            "billing_frequency": "Monthly",
            "delivery_frequency": "Weekly"
        },
        {
            "plan_name": "Daily Dairy Subscription",
            "plan_code": "DDD-001",
            "plan_type": "Custom",
            "base_price": 2999,
            "billing_frequency": "Monthly",
            "delivery_frequency": "Daily"
        }
    ]
    
    for plan in plans:
        if not frappe.db.exists("Subscription Plan", {"plan_code": plan["plan_code"]}):
            doc = frappe.new_doc("Subscription Plan")
            doc.update(plan)
            doc.is_active = 1
            doc.status = "Active"
            doc.insert()
    
    frappe.db.commit()
