import frappe
from frappe.model.document import Document
from frappe.utils import add_months, today, get_first_day, get_last_day

class SubscriptionBilling(Document):
    def validate(self):
        self.calculate_totals()
    
    def calculate_totals(self):
        sub_amount = self.subscription_amount or 0
        charges = self.additional_charges or 0
        discount = self.discount or 0
        self.total_amount = sub_amount + charges - discount
        self.balance_amount = self.total_amount - (self.paid_amount or 0)

@frappe.whitelist()
def generate_monthly_bills():
    first_day = get_first_day(today())
    last_day = get_last_day(today())
    
    subscriptions = frappe.get_all("Subscription",
        filters={
            "status": "Active",
            "docstatus": 1
        },
        pluck="name"
    )
    
    for sub_name in subscriptions:
        sub = frappe.get_doc("Subscription", sub_name)
        existing = frappe.get_all("Subscription Billing",
            filters={
                "subscription": sub_name,
                "billing_period_start": first_day
            }
        )
        if not existing:
            bill = frappe.new_doc("Subscription Billing")
            bill.subscription = sub_name
            bill.customer = sub.customer
            bill.billing_period_start = first_day
            bill.billing_period_end = last_day
            bill.subscription_amount = sub.total_amount
            bill.due_date = add_months(first_day, 1)
            bill.insert()
