import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_marketplace_data():
    """Get marketplace homepage data"""
    return {
        "featured_farms": frappe.get_all("Farm",
            filters={"status": "Active"},
            fields=["name", "farm_name", "farm_rating", "is_organic", "images", "city"],
            order_by="farm_rating desc",
            limit=6
        ),
        "featured_products": frappe.get_all("Product",
            filters={"status": "Active", "available_for_one_time": 1},
            fields=["name", "product_name", "selling_price", "unit", "product_image", "is_organic", "category"],
            order_by="modified desc",
            limit=8
        ),
        "subscription_plans": frappe.get_all("Subscription Plan",
            filters={"is_active": 1, "status": "Active"},
            fields=["name", "plan_name", "plan_type", "final_price", "billing_frequency", "description"],
            order_by="final_price asc"
        ),
        "categories": frappe.get_all("Product Category",
            filters={"is_active": 1},
            fields=["name", "category_name", "category_type"]
        )
    }

@frappe.whitelist(allow_guest=True)
def get_farm_detail(farm_name):
    """Get detailed farm information"""
    farm = frappe.get_doc("Farm", farm_name)
    products = frappe.get_all("Farm Product",
        filters={"farm": farm_name, "status": "Available"},
        fields=["name", "product_name", "selling_price", "unit", "quantity_available", "is_organic", "quality_grade"]
    )
    reviews = frappe.get_all("Customer Review",
        filters={"farm": farm_name, "is_approved": 1},
        fields=["customer_name", "rating", "review_title", "review_text", "review_date"],
        limit=10
    )
    return {
        "farm": farm.as_dict(),
        "products": products,
        "reviews": reviews
    }

@frappe.whitelist(allow_guest=True)
def get_product_detail(product_name):
    """Get detailed product information"""
    product = frappe.get_doc("Product", product_name)
    farms = frappe.get_all("Farm Product",
        filters={"product": product_name, "status": "Available"},
        fields=["name", "farm", "selling_price", "quantity_available", "farm_name"]
    )
    reviews = frappe.get_all("Customer Review",
        filters={"product": product_name, "is_approved": 1},
        fields=["customer_name", "rating", "review_title", "review_text", "review_date"],
        limit=10
    )
    return {
        "product": product.as_dict(),
        "farms": farms,
        "reviews": reviews
    }

@frappe.whitelist()
def create_customer_order(customer, items, delivery_address, delivery_zone=None, payment_mode="UPI", delivery_date=None, customer_notes=None):
    """Create a new order for customer"""
    order = frappe.new_doc("Order")
    order.customer = customer
    order.order_type = "One-time"
    order.delivery_address = delivery_address
    order.delivery_zone = delivery_zone
    order.payment_mode = payment_mode
    order.delivery_date = delivery_date or frappe.utils.today()
    order.customer_notes = customer_notes
    
    for item in items:
        product = frappe.get_doc("Product", item["product"])
        order.append("order_items", {
            "product": item["product"],
            "product_name": product.product_name,
            "quantity": item["quantity"],
            "unit": product.unit,
            "rate": product.selling_price,
            "amount": item["quantity"] * product.selling_price
        })
    
    order.insert()
    order.submit()
    return {"order_id": order.name, "status": order.status}

@frappe.whitelist()
def create_customer_subscription(customer, subscription_plan, start_date, delivery_address, delivery_time_slot=None, payment_mode="UPI"):
    """Create a new subscription for customer"""
    plan = frappe.get_doc("Subscription Plan", subscription_plan)
    
    subscription = frappe.new_doc("Subscription")
    subscription.customer = customer
    subscription.subscription_plan = subscription_plan
    subscription.start_date = start_date
    subscription.delivery_address = delivery_address
    subscription.delivery_time_slot = delivery_time_slot
    subscription.payment_mode = payment_mode
    subscription.subscription_amount = plan.final_price
    subscription.total_amount = plan.final_price
    subscription.balance_amount = plan.final_price
    
    for product in plan.subscription_products:
        subscription.append("subscription_products", {
            "product": product.product,
            "product_name": product.product_name,
            "quantity": product.quantity,
            "unit": product.unit,
            "price": product.price
        })
    
    subscription.insert()
    subscription.submit()
    return {"subscription_id": subscription.name, "status": subscription.status}

@frappe.whitelist()
def get_customer_dashboard(customer):
    """Get customer dashboard data"""
    return {
        "active_subscriptions": frappe.get_all("Subscription",
            filters={"customer": customer, "status": "Active", "docstatus": 1},
            fields=["name", "plan_name", "next_delivery_date", "total_amount", "balance_amount"]
        ),
        "recent_orders": frappe.get_all("Order",
            filters={"customer": customer, "docstatus": 1},
            fields=["name", "order_date", "status", "grand_total", "delivery_date"],
            order_by="order_date desc",
            limit=5
        ),
        "upcoming_deliveries": frappe.get_all("Delivery Schedule",
            filters={"customer": customer, "status": ["in", ["Scheduled", "Confirmed", "Out for Delivery"]]},
            fields=["name", "delivery_date", "delivery_time_slot", "status", "tracking_number"],
            order_by="delivery_date asc",
            limit=5
        ),
        "wallet_balance": get_wallet_balance(customer)
    }

def get_wallet_balance(customer):
    wallet = frappe.get_doc("Customer Wallet", {"customer": customer})
    return wallet.balance if wallet else 0

@frappe.whitelist()
def add_to_wishlist(customer, product):
    """Add product to customer wishlist"""
    wishlist = frappe.get_doc("Wishlist", {"customer": customer})
    if not wishlist:
        wishlist = frappe.new_doc("Wishlist")
        wishlist.customer = customer
    
    existing = [item for item in wishlist.wishlist_items if item.product == product]
    if existing:
        return {"status": "already_exists"}
    
    product_doc = frappe.get_doc("Product", product)
    wishlist.append("wishlist_items", {
        "product": product,
        "product_name": product_doc.product_name,
        "added_date": frappe.utils.today()
    })
    wishlist.save()
    return {"status": "added"}

@frappe.whitelist()
def get_delivery_tracking(tracking_number):
    """Get delivery tracking information"""
    delivery = frappe.get_all("Delivery Schedule",
        filters={"tracking_number": tracking_number},
        fields=["name", "status", "delivery_date", "delivery_time_slot", "actual_delivery_time", "delivery_agent", "agent_name"]
    )
    if delivery:
        return delivery[0]
    return None

@frappe.whitelist(allow_guest=True)
def search_products_and_farms(search_text=None, category=None, product_type=None, is_organic=None, city=None):
    """Search products and farms"""
    products = []
    farms = []
    
    if search_text or category or product_type or is_organic is not None:
        product_filters = {"status": "Active"}
        if category:
            product_filters["category"] = category
        if product_type:
            product_filters["product_type"] = product_type
        if is_organic is not None:
            product_filters["is_organic"] = is_organic
        
        products = frappe.get_all("Product", filters=product_filters,
            fields=["name", "product_name", "selling_price", "unit", "product_image", "is_organic", "category"])
        
        if search_text:
            products = [p for p in products if search_text.lower() in p.product_name.lower()]
    
    if search_text or city:
        farm_filters = {"status": "Active"}
        if city:
            farm_filters["city"] = city
        
        farms = frappe.get_all("Farm", filters=farm_filters,
            fields=["name", "farm_name", "farm_rating", "is_organic", "images", "city"])
        
        if search_text:
            farms = [f for f in farms if search_text.lower() in f.farm_name.lower()]
    
    return {"products": products, "farms": farms}
