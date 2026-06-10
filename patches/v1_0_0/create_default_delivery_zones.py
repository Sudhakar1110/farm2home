import frappe

def execute():
    zones = [
        {"zone_name": "Central City", "city": "Bangalore", "delivery_charge": 30},
        {"zone_name": "North Zone", "city": "Bangalore", "delivery_charge": 50},
        {"zone_name": "South Zone", "city": "Bangalore", "delivery_charge": 50},
        {"zone_name": "East Zone", "city": "Bangalore", "delivery_charge": 40},
        {"zone_name": "West Zone", "city": "Bangalore", "delivery_charge": 40}
    ]
    
    for zone in zones:
        if not frappe.db.exists("Delivery Zone", zone["zone_name"]):
            doc = frappe.new_doc("Delivery Zone")
            doc.update(zone)
            doc.is_active = 1
            doc.insert()
    
    frappe.db.commit()
