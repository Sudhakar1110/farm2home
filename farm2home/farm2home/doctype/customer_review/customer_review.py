from frappe.model.document import Document

class CustomerReview(Document):
    def on_update(self):
        if self.farm:
            self.update_farm_rating()
        if self.product:
            self.update_product_rating()
    
    def update_farm_rating(self):
        avg_rating = frappe.db.sql("""
            SELECT AVG(rating) FROM `tabCustomer Review`
            WHERE farm = %s AND is_approved = 1
        """, (self.farm,))[0][0]
        if avg_rating:
            farm = frappe.get_doc("Farm", self.farm)
            farm.customer_rating = avg_rating
            farm.save()
    
    def update_product_rating(self):
        avg_rating = frappe.db.sql("""
            SELECT AVG(rating) FROM `tabCustomer Review`
            WHERE product = %s AND is_approved = 1
        """, (self.product,))[0][0]
        if avg_rating:
            product = frappe.get_doc("Product", self.product)
            product.rating = avg_rating
            product.save()
