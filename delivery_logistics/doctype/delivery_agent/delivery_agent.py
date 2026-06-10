from frappe.model.document import Document

class DeliveryAgent(Document):
    def validate(self):
        self.agent_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
