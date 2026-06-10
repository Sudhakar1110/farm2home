from frappe.model.document import Document

class ProductInventory(Document):
    def validate(self):
        self.calculate_available_quantity()
    
    def calculate_available_quantity(self):
        self.available_quantity = (self.quantity or 0) - (self.reserved_quantity or 0)
