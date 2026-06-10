import frappe

def execute():
    categories = [
        "Organic Farm",
        "Dairy Farm",
        "Vegetable Farm",
        "Fruit Orchard",
        "Mixed Crop Farm",
        "Poultry Farm"
    ]
    
    for category in categories:
        if not frappe.db.exists("Farm Category", category):
            doc = frappe.new_doc("Farm Category")
            doc.category_name = category
            doc.is_active = 1
            doc.insert()
    
    frappe.db.commit()
