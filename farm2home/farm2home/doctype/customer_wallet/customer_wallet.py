import frappe
from frappe.model.document import Document

class CustomerWallet(Document):
    def validate(self):
        self.calculate_totals()
    
    def calculate_totals(self):
        credited = 0
        debited = 0
        for txn in self.transactions:
            if txn.transaction_type == "Credit":
                credited += txn.amount or 0
            else:
                debited += txn.amount or 0
        self.total_credited = credited
        self.total_debited = debited
        self.balance = credited - debited

@frappe.whitelist()
def add_wallet_balance(customer, amount, reference=None):
    wallet = frappe.get_doc("Customer Wallet", {"customer": customer})
    if not wallet:
        wallet = frappe.new_doc("Customer Wallet")
        wallet.customer = customer
    
    wallet.append("transactions", {
        "transaction_type": "Credit",
        "amount": amount,
        "reference": reference,
        "date": frappe.utils.now()
    })
    wallet.save()
    return wallet.balance

@frappe.whitelist()
def get_wallet_balance(customer):
    wallet = frappe.get_doc("Customer Wallet", {"customer": customer})
    return wallet.balance if wallet else 0
