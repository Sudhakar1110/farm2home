import frappe
from frappe.model.document import Document

class Product(Document):
    def validate(self):
        self.calculate_selling_price()
        self.validate_stock()
    
    def calculate_selling_price(self):
        if self.base_price and self.discount_percentage:
            self.selling_price = self.base_price * (1 - self.discount_percentage / 100)
        elif self.base_price:
            self.selling_price = self.base_price
    
    def validate_stock(self):
        if self.stock_quantity is not None and self.reorder_level is not None:
            if self.stock_quantity <= self.reorder_level:
                self.status = "Out of Stock"

@frappe.whitelist()
def get_product_price(product):
    product_doc = frappe.get_doc("Product", product)
    return {
        "selling_price": product_doc.selling_price,
        "mrp": product_doc.mrp,
        "discount": product_doc.discount_percentage,
        "unit": product_doc.unit
    }

@frappe.whitelist()
def search_products(category=None, product_type=None, is_organic=None, search_text=None):
    filters = {"status": "Active"}
    if category:
        filters["category"] = category
    if product_type:
        filters["product_type"] = product_type
    if is_organic is not None:
        filters["is_organic"] = is_organic
    
    products = frappe.get_all("Product", filters=filters, fields=["name", "product_name", "selling_price", "unit", "product_image", "is_organic"])
    
    if search_text:
        products = [p for p in products if search_text.lower() in p.product_name.lower()]
    
    return products
