app_name = "farm2home"
app_title = "Farm to Home"
app_publisher = "Farm2Home Team"
app_description = "Farm-to-Home Subscription Platform connecting farmers directly with customers"
app_email = "support@farm2home.local"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/farm2home/css/farm2home.css"
# app_include_js = "/assets/farm2home/js/farm2home.js"

# include js, css files in header of web template
# web_include_css = "/assets/farm2home/css/farm2home.css"
# web_include_js = "/assets/farm2home/js/farm2home.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "farm2home/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"Doctype": "public/js/doctype.js"}
# webform_include_css = {"Doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "farm2home.install.before_install"

# Workspace sync is handled automatically by frappe.model.sync.sync_all()
# during bench migrate/install-app. Workspace JSON files must be at:
# [app]/[module]/workspace/[name]/[name].json (directory = workspace, singular)
# after_migrate = []

# after_install = "farm2home.install.after_install"

# Uninstallation
# --------------

# before_uninstall = "farm2home.uninstall.before_uninstall"
# after_uninstall = "farm2home.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "farm2home.notifications.get_notification_config"

# Permissions
# -----------

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Subscription": {
        "on_submit": "farm2home.subscription_management.doctype.subscription.subscription.on_submit",
        "on_cancel": "farm2home.subscription_management.doctype.subscription.subscription.on_cancel",
    },
    "Order": {
        "on_submit": "farm2home.order_management.doctype.order.order.on_submit",
        "on_cancel": "farm2home.order_management.doctype.order.order.on_cancel",
    },
    "Payment Transaction": {
        "on_submit": "farm2home.payments.doctype.payment_transaction.payment_transaction.on_submit",
    },
    "Delivery Schedule": {
        "on_update": "farm2home.delivery_logistics.doctype.delivery_schedule.delivery_schedule.on_update",
    },
    "Quality Inspection": {
        "on_submit": "farm2home.quality_compliance.doctype.quality_inspection.quality_inspection.on_submit",
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "farm2home.subscription_management.doctype.subscription.subscription.process_daily_subscriptions",
        "farm2home.delivery_logistics.doctype.delivery_schedule.delivery_schedule.generate_daily_delivery_schedules",
        "farm2home.subscription_management.doctype.subscription_billing.subscription_billing.generate_monthly_bills",
    ],
    "hourly": [
        "farm2home.order_management.doctype.order.order.update_order_status",
    ],
    "weekly": [
        "farm2home.farm_management.doctype.farm.farm.update_farm_performance_metrics",
    ],
    "cron": {
        "0 6 * * *": [
            "farm2home.subscription_management.doctype.subscription.subscription.send_daily_reminders",
        ],
        "0 20 * * *": [
            "farm2home.delivery_logistics.doctype.delivery_schedule.delivery_schedule.optimize_routes",
        ],
    },
}

# Testing
# -------

# before_tests = "farm2home.install.before_tests"

# Overriding Methods
# ------------------

# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "farm2home.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "farm2home.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------

# before_request = ["farm2home.utils.before_request"]
# after_request = ["farm2home.utils.after_request"]

# Job Events
# ----------

# before_job = ["farm2home.utils.before_job"]
# after_job = ["farm2home.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#	},
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"farm2home.auth.validate"
# ]

# Fixtures
# --------

# IMPORTANT: Workflow States must be exported as fixtures BEFORE workflows that
# reference them. The fixtures below ensure all Workflow States referenced by
# Subscription, Order, Delivery Schedule, and Quality Inspection workflows exist.

fixtures = [
    "fixtures.role",
    "fixtures.workflow",
    "fixtures.module_def",
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "like", "%farm2home%"]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["name", "like", "%farm2home%"]
        ]
    },
    {
        "dt": "Role",
        "filters": [
            ["name", "in", ["Farm Manager", "Delivery Agent", "Customer", "Subscription Manager", "Quality Inspector", "Farm Admin"]]
        ]
    },
    {
        "dt": "Workflow",
        "filters": [
            ["document_type", "in", ["Subscription", "Order", "Delivery Schedule", "Quality Inspection"]]
        ]
    },
    {
        "dt": "Workflow State",
        "filters": [
            ["name", "in", ["Draft", "Active", "Paused", "Cancelled", "Pending", "Confirmed", "Out for Delivery", "Delivered", "Returned", "Inspected", "Approved", "Rejected"]]
        ]
    },
    {
        "dt": "Workflow Action Master",
        "filters": [
            ["name", "in", ["Approve", "Reject", "Cancel", "Resume", "Pause", "Confirm", "Deliver", "Return"]]
        ]
    },
    {
        "dt": "Notification",
        "filters": [
            ["document_type", "in", ["Subscription", "Order", "Delivery Schedule", "Payment Transaction", "Quality Inspection"]]
        ]
    },
    {
        "dt": "Email Template",
        "filters": [
            ["name", "like", "%Farm2Home%"]
        ]
    },
    {
        "dt": "Print Format",
        "filters": [
            ["doc_type", "in", ["Order", "Subscription", "Delivery Schedule", "Payment Transaction"]]
        ]
    },
    {
        "dt": "Web Form",
        "filters": [
            ["module", "=", "Farm to Home"]
        ]
    },
    {
        "dt": "Dashboard Chart",
        "filters": [
            ["chart_name", "like", "%Farm2Home%"]
        ]
    },
    {
        "dt": "Number Card",
        "filters": [
            ["name", "like", "%Farm2Home%"]
        ]
    },
]

# Website Route Rules
# -------------------

# website_route_rules = [
#     {"from_route": "/farm/<path:farm_name>", "to_route": "farm_profile"},
#     {"from_route": "/product/<path:product_name>", "to_route": "product_detail"},
# ]

# Jinja Filters
# -------------

# jinja = {
#     "methods": [
#         "farm2home.utils.jinja_filters",
#     ]
# }
