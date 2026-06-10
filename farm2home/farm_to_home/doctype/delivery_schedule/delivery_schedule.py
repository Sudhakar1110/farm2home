import frappe
from frappe.model.document import Document
from frappe.utils import today, now, random_string

class DeliverySchedule(Document):
    def validate(self):
        if self.delivery_address:
            address = frappe.get_doc("Address", self.delivery_address)
            self.address_display = address.display_address
    
    def on_update(self):
        if self.status == "Out for Delivery" and not self.tracking_number:
            self.tracking_number = random_string(10).upper()
        if self.status == "Delivered" and not self.actual_delivery_time:
            self.actual_delivery_time = now()
        self.update_linked_documents()
    
    def update_linked_documents(self):
        if self.order:
            order = frappe.get_doc("Order", self.order)
            if self.status == "Delivered":
                order.status = "Delivered"
                order.save()
        if self.subscription:
            sub = frappe.get_doc("Subscription", self.subscription)
            sub.last_delivery_date = today()
            sub.save()

@frappe.whitelist()
def generate_daily_delivery_schedules():
    date = today()
    subscriptions = frappe.get_all("Subscription",
        filters={
            "status": "Active",
            "docstatus": 1,
            "next_delivery_date": date
        },
        pluck="name"
    )
    for sub_name in subscriptions:
        sub = frappe.get_doc("Subscription", sub_name)
        if not sub.is_paused:
            create_delivery_schedule(sub)

def create_delivery_schedule(subscription):
    existing = frappe.get_all("Delivery Schedule",
        filters={
            "subscription": subscription.name,
            "delivery_date": today()
        }
    )
    if existing:
        return
    
    delivery = frappe.new_doc("Delivery Schedule")
    delivery.subscription = subscription.name
    delivery.customer = subscription.customer
    delivery.delivery_address = subscription.delivery_address
    delivery.delivery_zone = subscription.delivery_zone
    delivery.delivery_date = today()
    delivery.delivery_time_slot = subscription.delivery_time_slot
    delivery.status = "Scheduled"
    delivery.delivery_otp = random_string(4).upper()
    
    for product in subscription.subscription_products:
        delivery.append("delivery_items", {
            "product": product.product,
            "product_name": product.product_name,
            "quantity": product.quantity,
            "unit": product.unit
        })
    
    delivery.insert()

@frappe.whitelist()
def optimize_routes():
    tomorrow = frappe.utils.add_days(today(), 1)
    deliveries = frappe.get_all("Delivery Schedule",
        filters={"delivery_date": tomorrow, "status": "Scheduled"},
        fields=["name", "delivery_zone"]
    )
    zones = {}
    for d in deliveries:
        zone = d.delivery_zone or "Default"
        if zone not in zones:
            zones[zone] = []
        zones[zone].append(d.name)
    
    for zone, delivery_list in zones.items():
        for idx, delivery_name in enumerate(delivery_list):
            delivery = frappe.get_doc("Delivery Schedule", delivery_name)
            delivery.delivery_route = f"ROUTE-{zone}-{tomorrow}"
            delivery.save()

@frappe.whitelist()
def confirm_delivery(delivery, otp=None, notes=None):
    delivery_doc = frappe.get_doc("Delivery Schedule", delivery)
    if delivery_doc.otp_verification and delivery_doc.delivery_otp != otp:
        frappe.throw("Invalid OTP")
    delivery_doc.status = "Delivered"
    delivery_doc.actual_delivery_time = now()
    delivery_doc.delivery_confirmation = "Confirmed"
    if notes:
        delivery_doc.delivery_notes = notes
    delivery_doc.save()
    return "Delivery confirmed successfully"
