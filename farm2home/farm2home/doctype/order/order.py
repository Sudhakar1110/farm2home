import frappe
from frappe.model.document import Document
from frappe.utils import today

class Order(Document):
    def validate(self):
        self.calculate_totals()
        self.validate_items()
    
    def on_submit(self):
        self.status = "Confirmed"
        self.create_delivery_schedule()
        self.update_inventory()
    
    def on_cancel(self):
        self.status = "Cancelled"
        self.restore_inventory()
    
    def calculate_totals(self):
        subtotal = 0
        for item in self.order_items:
            item.amount = (item.quantity or 0) * (item.rate or 0)
            subtotal += item.amount
        
        self.subtotal = subtotal
        tax = self.tax_amount or 0
        delivery = self.delivery_charge or 0
        discount = self.discount_amount or 0
        self.grand_total = subtotal + tax + delivery - discount
        self.balance_amount = self.grand_total - (self.paid_amount or 0)
    
    def validate_items(self):
        if not self.order_items:
            frappe.throw("Please add at least one item to the order")
    
    def create_delivery_schedule(self):
        if self.delivery_date:
            delivery = frappe.new_doc("Delivery Schedule")
            delivery.order = self.name
            delivery.customer = self.customer
            delivery.delivery_address = self.delivery_address
            delivery.delivery_zone = self.delivery_zone
            delivery.delivery_date = self.delivery_date
            delivery.delivery_time_slot = self.delivery_time_slot
            delivery.status = "Scheduled"
            
            for item in self.order_items:
                delivery.append("delivery_items", {
                    "product": item.product,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit": item.unit
                })
            
            delivery.insert()
    
    def update_inventory(self):
        for item in self.order_items:
            if item.product:
                product = frappe.get_doc("Product", item.product)
                if product.stock_quantity is not None:
                    product.stock_quantity -= (item.quantity or 0)
                    product.save()
    
    def restore_inventory(self):
        for item in self.order_items:
            if item.product:
                product = frappe.get_doc("Product", item.product)
                if product.stock_quantity is not None:
                    product.stock_quantity += (item.quantity or 0)
                    product.save()

@frappe.whitelist()
def update_order_status():
    orders = frappe.get_all("Order",
        filters={
            "status": ["in", ["Confirmed", "Processing", "Out for Delivery"]],
            "docstatus": 1
        },
        pluck="name"
    )
    for order_name in orders:
        order = frappe.get_doc("Order", order_name)
        deliveries = frappe.get_all("Delivery Schedule",
            filters={"order": order_name},
            fields=["status"]
        )
        if deliveries:
            latest_status = deliveries[0].status
            if latest_status == "Delivered" and order.status != "Delivered":
                order.status = "Delivered"
                order.save()
            elif latest_status == "Out for Delivery" and order.status == "Confirmed":
                order.status = "Out for Delivery"
                order.save()

@frappe.whitelist()
def get_customer_orders(customer):
    return frappe.get_all("Order",
        filters={"customer": customer, "docstatus": 1},
        fields=["name", "order_date", "status", "grand_total", "delivery_date"],
        order_by="order_date desc"
    )
