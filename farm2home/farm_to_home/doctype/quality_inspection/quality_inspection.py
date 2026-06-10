import frappe
from frappe.model.document import Document

class QualityInspection(Document):
    def on_submit(self):
        if self.result == "Pass":
            self.status = "Approved"
        elif self.result == "Fail":
            self.status = "Rejected"
        else:
            self.status = "Inspected"
        self.update_product_grade()
    
    def update_product_grade(self):
        if self.product and self.overall_grade:
            product = frappe.get_doc("Product", self.product)
            product.quality_grade = self.overall_grade
            product.save()

@frappe.whitelist()
def create_quality_inspection(product, farm=None):
    inspection = frappe.new_doc("Quality Inspection")
    inspection.product = product
    inspection.farm = farm
    inspection.inspection_date = frappe.utils.today()
    inspection.insert()
    return inspection.name
