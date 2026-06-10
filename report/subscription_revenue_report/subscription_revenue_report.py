import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Subscription Plan"), "fieldname": "subscription_plan", "fieldtype": "Link", "options": "Subscription Plan", "width": 150},
        {"label": _("Plan Type"), "fieldname": "plan_type", "fieldtype": "Data", "width": 120},
        {"label": _("Total Subscriptions"), "fieldname": "total_subscriptions", "fieldtype": "Int", "width": 150},
        {"label": _("Total Revenue"), "fieldname": "total_revenue", "fieldtype": "Currency", "width": 150},
        {"label": _("Active Subscriptions"), "fieldname": "active_subscriptions", "fieldtype": "Int", "width": 150},
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql("""
        SELECT 
            s.subscription_plan,
            sp.plan_type,
            COUNT(s.name) as total_subscriptions,
            SUM(s.total_amount) as total_revenue,
            SUM(CASE WHEN s.status = 'Active' THEN 1 ELSE 0 END) as active_subscriptions
        FROM `tabSubscription` s
        LEFT JOIN `tabSubscription Plan` sp ON sp.name = s.subscription_plan
        WHERE s.docstatus = 1 {conditions}
        GROUP BY s.subscription_plan, sp.plan_type
        ORDER BY total_revenue DESC
    """.format(conditions=conditions), filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND s.start_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND s.start_date <= %(to_date)s"
    if filters.get("plan_type"):
        conditions += " AND sp.plan_type = %(plan_type)s"
    return conditions
