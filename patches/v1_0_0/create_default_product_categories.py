import frappe

def execute():
    categories = [
        {"name": "Vegetables", "type": "Vegetables"},
        {"name": "Fruits", "type": "Fruits"},
        {"name": "Dairy", "type": "Dairy"},
        {"name": "Grains", "type": "Grains"},
        {"name": "Pulses", "type": "Pulses"},
        {"name": "Spices", "type": "Spices"},
        {"name": "Herbs", "type": "Herbs"},
        {"name": "Organic", "type": "Organic"}
    ]
    
    for cat in categories:
        if not frappe.db.exists("Product Category", cat["name"]):
            doc = frappe.new_doc("Product Category")
            doc.category_name = cat["name"]
            doc.category_type = cat["type"]
            doc.is_active = 1
            doc.insert()
    
    frappe.db.commit()
