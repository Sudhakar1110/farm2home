import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Order Date"), "fieldname": "order_date", "fieldtype": "Date", "width": 120},
        {"label": _("Order Type"), "fieldname": "order_type", "fieldtype": "Data", "width": 120},
        {"label": _("Total Orders"), "fieldname": "total_orders", "fieldtype": "Int", "width": 120},
        {"label": _("Total Revenue"), "fieldname": "total_revenue", "fieldtype": "Currency", "width": 150},
        {"label": _("Total Items"), "fieldname": "total_items", "fieldtype": "Int", "width": 120},
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql("""
        SELECT 
            o.order_date,
            o.order_type,
            COUNT(DISTINCT o.name) as total_orders,
            SUM(o.grand_total) as total_revenue,
            COUNT(oi.name) as total_items
        FROM `tabOrder` o
        LEFT JOIN `tabOrder Item` oi ON oi.parent = o.name
        WHERE o.docstatus = 1 {conditions}
        GROUP BY o.order_date, o.order_type
        ORDER BY o.order_date DESC
    """.format(conditions=conditions), filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND o.order_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND o.order_date <= %(to_date)s"
    if filters.get("farm"):
        conditions += " AND o.farm = %(farm)s"
    if filters.get("order_type"):
        conditions += " AND o.order_type = %(order_type)s"
    return conditions
