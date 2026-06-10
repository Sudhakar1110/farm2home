import frappe
from frappe.model.document import Document

class Farmer(Document):
    def validate(self):
        self.set_full_name()
        self.validate_phone()
    
    def set_full_name(self):
        self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
    
    def validate_phone(self):
        if self.phone:
            self.phone = self.phone.strip()
            if len(self.phone) < 10:
                frappe.throw("Phone number must be at least 10 digits")

@frappe.whitelist()
def get_farmer_farms(farmer):
    return frappe.get_all("Farm Farmer",
        filters={"parent": farmer},
        fields=["farm"]
    )
