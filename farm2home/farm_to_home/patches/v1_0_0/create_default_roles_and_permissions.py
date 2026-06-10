import frappe
from frappe.permissions import add_permission

def execute():
    roles = ["Farm Manager", "Delivery Agent", "Customer", "Subscription Manager", "Quality Inspector", "Farm Admin"]
    
    for role in roles:
        if not frappe.db.exists("Role", role):
            doc = frappe.new_doc("Role")
            doc.role_name = role
            doc.desk_access = 1
            doc.insert()
    
    frappe.db.commit()
