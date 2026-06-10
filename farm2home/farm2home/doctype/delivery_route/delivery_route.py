from frappe.model.document import Document

class DeliveryRoute(Document):
    def validate(self):
        self.total_stops = len(self.route_deliveries) if self.route_deliveries else 0
