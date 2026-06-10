import frappe
from frappe.model.document import Document

class PaymentTransaction(Document):
    def validate(self):
        self.calculate_total()
    
    def on_submit(self):
        self.status = "Completed"
        self.update_order_payment()
        self.update_subscription_payment()
        self.update_wallet()
    
    def calculate_total(self):
        self.total_amount = (self.amount or 0) + (self.transaction_fee or 0)
    
    def update_order_payment(self):
        if self.order:
            order = frappe.get_doc("Order", self.order)
            order.paid_amount = (order.paid_amount or 0) + self.amount
            if order.paid_amount >= order.grand_total:
                order.payment_status = "Paid"
            else:
                order.payment_status = "Partially Paid"
            order.save()
    
    def update_subscription_payment(self):
        if self.subscription:
            sub = frappe.get_doc("Subscription", self.subscription)
            sub.paid_amount = (sub.paid_amount or 0) + self.amount
            sub.total_payments = (sub.total_payments or 0) + self.amount
            sub.balance_amount = sub.total_amount - sub.paid_amount
            sub.save()
    
    def update_wallet(self):
        if self.payment_mode == "Wallet":
            wallet = frappe.get_doc("Customer Wallet", {"customer": self.customer})
            if wallet:
                wallet.balance -= self.amount
                wallet.append("transactions", {
                    "transaction_type": "Debit",
                    "amount": self.amount,
                    "reference": self.name,
                    "date": self.payment_date
                })
                wallet.save()

@frappe.whitelist()
def process_refund(payment_transaction, amount, reason=None):
    payment = frappe.get_doc("Payment Transaction", payment_transaction)
    if payment.status != "Completed":
        frappe.throw("Only completed payments can be refunded")
    
    payment.is_refunded = 1
    payment.refund_amount = amount
    payment.refund_date = frappe.utils.today()
    payment.refund_reason = reason
    payment.status = "Refunded"
    payment.save()
    
    if payment.order:
        order = frappe.get_doc("Order", payment.order)
        order.paid_amount -= amount
        if order.paid_amount <= 0:
            order.payment_status = "Pending"
        order.save()
    
    return "Refund processed successfully"
