import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today, getdate

class Subscription(Document):
    def validate(self):
        self.calculate_totals()
        self.validate_dates()
        self.set_subscription_type()
    
    def on_submit(self):
        self.status = "Active"
        self.create_initial_delivery_schedule()
    
    def on_cancel(self):
        self.status = "Cancelled"
        self.cancel_future_deliveries()
    
    def calculate_totals(self):
        amount = self.subscription_amount or 0
        discount = self.discount_applied or 0
        self.total_amount = amount - discount
        self.balance_amount = self.total_amount - (self.paid_amount or 0)
    
    def validate_dates(self):
        if self.end_date and getdate(self.start_date) > getdate(self.end_date):
            frappe.throw("End Date cannot be before Start Date")
    
    def set_subscription_type(self):
        if self.subscription_plan:
            plan = frappe.get_doc("Subscription Plan", self.subscription_plan)
            self.subscription_type = plan.plan_type
            self.billing_frequency = plan.billing_frequency
    
    def create_initial_delivery_schedule(self):
        if self.delivery_day == "Daily":
            next_date = add_days(getdate(self.start_date), 1)
        else:
            next_date = self.start_date
        self.next_delivery_date = next_date
    
    def cancel_future_deliveries(self):
        deliveries = frappe.get_all("Delivery Schedule",
            filters={
                "subscription": self.name,
                "status": ["in", ["Scheduled", "Pending"]],
                "delivery_date": [">=", today()]
            },
            pluck="name"
        )
        for delivery in deliveries:
            doc = frappe.get_doc("Delivery Schedule", delivery)
            doc.status = "Cancelled"
            doc.save()

@frappe.whitelist()
def process_daily_subscriptions():
    subscriptions = frappe.get_all("Subscription",
        filters={
            "status": "Active",
            "docstatus": 1,
            "next_delivery_date": today()
        },
        pluck="name"
    )
    for sub_name in subscriptions:
        sub = frappe.get_doc("Subscription", sub_name)
        if not sub.is_paused:
            create_delivery_for_subscription(sub)
            update_next_delivery_date(sub)

def create_delivery_for_subscription(subscription):
    delivery = frappe.new_doc("Delivery Schedule")
    delivery.subscription = subscription.name
    delivery.customer = subscription.customer
    delivery.delivery_address = subscription.delivery_address
    delivery.delivery_zone = subscription.delivery_zone
    delivery.delivery_date = today()
    delivery.delivery_time_slot = subscription.delivery_time_slot
    delivery.status = "Scheduled"
    
    for product in subscription.subscription_products:
        delivery.append("delivery_items", {
            "product": product.product,
            "product_name": product.product_name,
            "quantity": product.quantity,
            "unit": product.unit
        })
    
    delivery.insert()
    frappe.db.commit()

def update_next_delivery_date(subscription):
    if subscription.delivery_day == "Daily":
        subscription.next_delivery_date = add_days(getdate(subscription.next_delivery_date), 1)
    elif subscription.delivery_day == "Alternate Days":
        subscription.next_delivery_date = add_days(getdate(subscription.next_delivery_date), 2)
    else:
        subscription.next_delivery_date = add_days(getdate(subscription.next_delivery_date), 7)
    subscription.last_delivery_date = today()
    subscription.total_deliveries = (subscription.total_deliveries or 0) + 1
    subscription.save()

@frappe.whitelist()
def pause_subscription(subscription, start_date, end_date, reason=None):
    sub = frappe.get_doc("Subscription", subscription)
    sub.is_paused = 1
    sub.pause_start_date = start_date
    sub.pause_end_date = end_date
    sub.pause_reason = reason
    sub.status = "Paused"
    sub.save()
    return "Subscription paused successfully"

@frappe.whitelist()
def resume_subscription(subscription):
    sub = frappe.get_doc("Subscription", subscription)
    sub.is_paused = 0
    sub.pause_start_date = None
    sub.pause_end_date = None
    sub.pause_reason = None
    sub.status = "Active"
    sub.save()
    return "Subscription resumed successfully"

@frappe.whitelist()
def send_daily_reminders():
    tomorrow = add_days(today(), 1)
    subscriptions = frappe.get_all("Subscription",
        filters={
            "status": "Active",
            "docstatus": 1,
            "next_delivery_date": tomorrow
        },
        fields=["name", "customer", "customer_name"]
    )
    for sub in subscriptions:
        customer = frappe.get_doc("Customer", sub.customer)
        if customer.email_id:
            frappe.sendmail(
                recipients=[customer.email_id],
                subject="Your Farm2Home Delivery Tomorrow",
                message=f"Dear {sub.customer_name}, your fresh produce delivery is scheduled for tomorrow."
            )
