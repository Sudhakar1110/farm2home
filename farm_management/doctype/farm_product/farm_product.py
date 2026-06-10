import frappe
from frappe.model.document import Document

class FarmProduct(Document):
    def validate(self):
        self.calculate_selling_price()
        self.update_product_link()
    
    def calculate_selling_price(self):
        if self.farmer_price and self.platform_commission:
            commission = self.farmer_price * (self.platform_commission / 100)
            self.selling_price = self.farmer_price + commission
    
    def update_product_link(self):
        if self.product:
            product_doc = frappe.get_doc("Product", self.product)
            self.product_name = product_doc.product_name
            self.product_code = product_doc.product_code

@frappe.whitelist()
def get_farm_products_by_farm(farm):
    return frappe.get_all("Farm Product",
        filters={"farm": farm, "status": "Available"},
        fields=["name", "product_name", "selling_price", "unit", "quantity_available", "is_organic"]
    )
