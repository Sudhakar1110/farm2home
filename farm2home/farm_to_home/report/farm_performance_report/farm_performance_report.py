import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Farm"), "fieldname": "farm", "fieldtype": "Link", "options": "Farm", "width": 150},
        {"label": _("Farm Name"), "fieldname": "farm_name", "fieldtype": "Data", "width": 150},
        {"label": _("Total Products"), "fieldname": "total_products", "fieldtype": "Int", "width": 120},
        {"label": _("Total Orders"), "fieldname": "total_orders", "fieldtype": "Int", "width": 120},
        {"label": _("Total Revenue"), "fieldname": "total_revenue", "fieldtype": "Currency", "width": 150},
        {"label": _("Customer Rating"), "fieldname": "customer_rating", "fieldtype": "Rating", "width": 120},
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql("""
        SELECT 
            f.name as farm,
            f.farm_name,
            COUNT(DISTINCT fp.name) as total_products,
            COUNT(DISTINCT o.name) as total_orders,
            COALESCE(SUM(o.grand_total), 0) as total_revenue,
            f.customer_rating
        FROM `tabFarm` f
        LEFT JOIN `tabFarm Product` fp ON fp.farm = f.name AND fp.status = 'Available'
        LEFT JOIN `tabOrder` o ON o.farm = f.name AND o.docstatus = 1 {conditions}
        GROUP BY f.name, f.farm_name
        ORDER BY total_revenue DESC
    """.format(conditions=conditions), filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND o.order_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND o.order_date <= %(to_date)s"
    return conditions
