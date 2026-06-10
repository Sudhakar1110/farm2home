import frappe
from frappe.model.document import Document

class Farm(Document):
    def validate(self):
        self.validate_farm_code()
        self.update_last_updated()
    
    def on_update(self):
        self.update_performance_metrics()
    
    def validate_farm_code(self):
        if self.farm_code:
            self.farm_code = self.farm_code.upper().strip()
    
    def update_last_updated(self):
        self.last_updated = frappe.utils.now()
    
    def update_performance_metrics(self):
        self.total_products = frappe.db.count("Farm Product", {"farm": self.name})
        self.total_orders = frappe.db.count("Order", {"farm": self.name})
        total_rev = frappe.db.sql("""
            SELECT SUM(grand_total) FROM `tabOrder` 
            WHERE farm = %s AND docstatus = 1
        """, (self.name,))
        self.total_revenue = total_rev[0][0] if total_rev and total_rev[0][0] else 0
    
    def update_farm_performance_metrics():
        farms = frappe.get_all("Farm", pluck="name")
        for farm_name in farms:
            farm = frappe.get_doc("Farm", farm_name)
            farm.update_performance_metrics()
            farm.save()

@frappe.whitelist()
def get_farm_products(farm):
    return frappe.get_all("Farm Product", 
        filters={"farm": farm, "status": "Active"},
        fields=["name", "product_name", "category", "price", "unit"]
    )

@frappe.whitelist()
def get_farm_dashboard_data(farm):
    products = frappe.db.count("Farm Product", {"farm": farm})
    orders = frappe.db.count("Order", {"farm": farm})
    subscriptions = frappe.db.count("Subscription", {"farm": farm})
    revenue = frappe.db.sql("""
        SELECT SUM(grand_total) FROM `tabOrder` WHERE farm = %s AND docstatus = 1
    """, (farm,))[0][0] or 0
    
    return {
        "products": products,
        "orders": orders,
        "subscriptions": subscriptions,
        "revenue": revenue
    }
