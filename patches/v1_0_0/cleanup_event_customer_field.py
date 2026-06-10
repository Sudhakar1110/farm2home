import frappe


def execute():
    """Remove leftover event_customer field from Customer doctype.

    This field was left behind by a previously uninstalled app (Event Booking Platform)
    and references a non-existing doctype 'Event Customer'. It causes errors when
    opening the Customer form in Frappe Desk.
    """
    field_name = "event_customer"
    doctype = "Customer"

    # Check if the custom field exists
    if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
        frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Removed leftover custom field '{field_name}' from {doctype} doctype")

    # Also check for property setter references
    if frappe.db.exists("Property Setter", {"doc_type": doctype, "field_name": field_name}):
        frappe.delete_doc("Property Setter", f"{doctype}-{field_name}-field_type", ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Removed leftover property setter for '{field_name}' from {doctype} doctype")

    # Check for any other leftover event_* fields
    for leftover in frappe.get_all("Custom Field", filters={"dt": doctype, "fieldname": ("like", "event_%")}, pluck="name"):
        frappe.delete_doc("Custom Field", leftover, ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Removed leftover custom field '{leftover}' from {doctype} doctype")
