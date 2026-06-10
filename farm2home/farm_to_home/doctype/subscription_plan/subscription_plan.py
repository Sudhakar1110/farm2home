from frappe.model.document import Document

class SubscriptionPlan(Document):
    def validate(self):
        self.calculate_final_price()
    
    def calculate_final_price(self):
        discount = self.discount_amount or 0
        self.final_price = (self.base_price or 0) - discount
        if self.final_price < 0:
            self.final_price = 0
