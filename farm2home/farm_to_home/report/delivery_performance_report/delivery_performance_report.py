import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Delivery Agent"), "fieldname": "delivery_agent", "fieldtype": "Link", "options": "Delivery Agent", "width": 150},
        {"label": _("Agent Name"), "fieldname": "agent_name", "fieldtype": "Data", "width": 150},
        {"label": _("Total Deliveries"), "fieldname": "total_deliveries", "fieldtype": "Int", "width": 120},
        {"label": _("Delivered"), "fieldname": "delivered", "fieldtype": "Int", "width": 100},
        {"label": _("Failed"), "fieldname": "failed", "fieldtype": "Int", "width": 100},
        {"label": _("Delivery Rate"), "fieldname": "delivery_rate", "fieldtype": "Percent", "width": 120},
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql("""
        SELECT 
            ds.delivery_agent,
            da.agent_name,
            COUNT(ds.name) as total_deliveries,
            SUM(CASE WHEN ds.status = 'Delivered' THEN 1 ELSE 0 END) as delivered,
            SUM(CASE WHEN ds.status = 'Failed' THEN 1 ELSE 0 END) as failed,
            ROUND(SUM(CASE WHEN ds.status = 'Delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(ds.name), 2) as delivery_rate
        FROM `tabDelivery Schedule` ds
        LEFT JOIN `tabDelivery Agent` da ON da.name = ds.delivery_agent
        WHERE 1=1 {conditions}
        GROUP BY ds.delivery_agent, da.agent_name
        ORDER BY total_deliveries DESC
    """.format(conditions=conditions), filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND ds.delivery_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND ds.delivery_date <= %(to_date)s"
    return conditions
