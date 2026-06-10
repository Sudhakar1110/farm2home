"""
Farm2Home Demo Data Generator

Generates realistic, fully-linked demo data for all custom Farm2Home DocTypes.
Uses standard ERPNext DocTypes (Customer, Address, Warehouse, etc.) where applicable.

Usage:
    bench --site sudhakar1.site execute farm2home.farm_to_home.demo_data.create_demo_data
"""

import frappe
import random
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


# ──────────────────────────────────────────────
# Data Constants
# ──────────────────────────────────────────────

INDIAN_CITIES = [
    ("Mumbai", "Maharashtra", "400001"),
    ("Delhi", "Delhi", "110001"),
    ("Bangalore", "Karnataka", "560001"),
    ("Hyderabad", "Telangana", "500001"),
    ("Chennai", "Tamil Nadu", "600001"),
    ("Kolkata", "West Bengal", "700001"),
    ("Pune", "Maharashtra", "411001"),
    ("Ahmedabad", "Gujarat", "380001"),
    ("Jaipur", "Rajasthan", "302001"),
    ("Lucknow", "Uttar Pradesh", "226001"),
    ("Surat", "Gujarat", "395001"),
    ("Indore", "Madhya Pradesh", "452001"),
    ("Bhopal", "Madhya Pradesh", "462001"),
    ("Nagpur", "Maharashtra", "440001"),
    ("Patna", "Bihar", "800001"),
    ("Vadodara", "Gujarat", "390001"),
    ("Visakhapatnam", "Andhra Pradesh", "530001"),
    ("Thiruvananthapuram", "Kerala", "695001"),
    ("Coimbatore", "Tamil Nadu", "641001"),
    ("Chandigarh", "Punjab", "160001"),
]

FARM_NAMES = [
    "Green Valley Farms",
    "Sunrise Organic Farm",
    "Nature Fresh Farms",
    "Golden Harvest Farm",
    "EcoLife Organics",
    "Green Earth Farms",
    "Pure Harvest Organics",
    "Fresh Fields Farm",
    "Bharat Naturals Farm",
    "Sahyadri Fresh Produce",
]

FARM_CATEGORIES = [
    "Organic Farm",
    "Vegetable Farm",
    "Dairy Farm",
    "Mixed Farm",
    "Fruit Orchard",
    "Poultry Farm",
    "Grain Farm",
    "Herbal Farm",
    "Integrated Farm",
    "Family Farm",
]

CERTIFICATIONS = [
    ("India Organic (NPOP)", "APEDA"),
    ("Jaivik Bharat", "Ministry of Commerce"),
    ("USDA Organic", "USDA"),
    ("EU Organic", "European Commission"),
    ("Global G.A.P.", "GLOBALG.A.P."),
    ("Rainforest Alliance", "Rainforest Alliance"),
    ("Fair Trade Certified", "Fair Trade India"),
    ("Biodynamic (Demeter)", "Demeter Association"),
    ("Non-GMO Project Verified", "Non-GMO Project"),
    ("Organic Farming (PKV)", "PKV Certification"),
    ("Natural Farming Certified", "ANDN"),
    ("PGS-India Organic", "PGS India"),
    ("Participatory Guarantee System", "IFOAM"),
    ("OneCert Asia Organic", "OneCert"),
    ("Control Union Organic", "Control Union"),
]

FIRST_NAMES_MALE = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Shaurya",
    "Yash", "Dhruv", "Rohan", "Krishna", "Amit", "Rajesh", "Suresh",
    "Mahesh", "Ramesh", "Dinesh", "Sunil", "Vijay", "Anil", "Sanjay",
    "Prakash", "Nilesh", "Ganesh", "Ravi",
]

FIRST_NAMES_FEMALE = [
    "Aanya", "Anaya", "Diya", "Isha", "Myra", "Priya", "Neha",
    "Sneha", "Anita", "Sunita", "Kavita", "Pooja", "Ritu",
    "Geeta", "Nandini", "Vandana", "Lakshmi", "Radha", "Meena", "Shweta",
    "Deepika", "Anjali", "Rekha", "Asha", "Shanti",
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Singh", "Kumar", "Gupta", "Reddy",
    "Nair", "Joshi", "Deshmukh", "Mehta", "Shah", "Agarwal", "Rao",
    "Menon", "Pillai", "Iyer", "Naidu", "Bose", "Sen", "Das",
    "Choudhury", "Mukherjee", "Banerjee", "Mitra",
]

PRODUCT_CATEGORIES = [
    ("Leafy Greens", "Vegetables"),
    ("Root Vegetables", "Vegetables"),
    ("Cruciferous Vegetables", "Vegetables"),
    ("Herbs & Spices", "Spices"),
    ("Seasonal Vegetables", "Vegetables"),
    ("Citrus Fruits", "Fruits"),
    ("Tropical Fruits", "Fruits"),
    ("Berries & Grapes", "Fruits"),
    ("Dairy Products", "Dairy"),
    ("Milk & Cream", "Dairy"),
    ("Grain Products", "Grains"),
    ("Pulses & Lentils", "Pulses"),
    ("Organic Vegetables", "Organic"),
    ("Organic Fruits", "Organic"),
    ("Exotic Vegetables", "Vegetables"),
]

PRODUCTS = [
    # (name, category_name, type, unit, price, organic)
    ("Organic Tomato", "Seasonal Vegetables", "Vegetable", "Kg", 40, 1),
    ("Fresh Onion", "Root Vegetables", "Vegetable", "Kg", 35, 1),
    ("Carrot", "Root Vegetables", "Vegetable", "Kg", 45, 1),
    ("Potato", "Root Vegetables", "Vegetable", "Kg", 25, 0),
    ("Green Chilli", "Herbs & Spices", "Vegetable", "Kg", 60, 1),
    ("Red Capsicum", "Exotic Vegetables", "Vegetable", "Kg", 80, 1),
    ("Yellow Capsicum", "Exotic Vegetables", "Vegetable", "Kg", 90, 1),
    ("Cauliflower", "Cruciferous Vegetables", "Vegetable", "Piece", 50, 0),
    ("Cabbage", "Cruciferous Vegetables", "Vegetable", "Piece", 35, 0),
    ("Broccoli", "Exotic Vegetables", "Vegetable", "Kg", 120, 1),
    ("Spinach", "Leafy Greens", "Vegetable", "Bunch", 25, 1),
    ("Coriander Leaves", "Herbs & Spices", "Vegetable", "Bunch", 15, 1),
    ("Mint Leaves", "Herbs & Spices", "Herb", "Bunch", 20, 1),
    ("Beetroot", "Root Vegetables", "Vegetable", "Kg", 40, 1),
    ("Radish", "Root Vegetables", "Vegetable", "Bunch", 30, 0),
    ("Banana", "Tropical Fruits", "Fruit", "Dozen", 50, 0),
    ("Mango (Alphonso)", "Tropical Fruits", "Fruit", "Kg", 150, 1),
    ("Apple (Shimla)", "Tropical Fruits", "Fruit", "Kg", 120, 0),
    ("Orange (Nagpur)", "Citrus Fruits", "Fruit", "Kg", 80, 1),
    ("Pomegranate", "Tropical Fruits", "Fruit", "Kg", 100, 0),
    ("Grapes (Bangalore)", "Berries & Grapes", "Fruit", "Kg", 90, 0),
    ("Papaya", "Tropical Fruits", "Fruit", "Kg", 50, 1),
    ("Watermelon", "Tropical Fruits", "Fruit", "Kg", 30, 0),
    ("Sweet Lime", "Citrus Fruits", "Fruit", "Kg", 60, 1),
    ("Coconut (Tender)", "Tropical Fruits", "Fruit", "Piece", 30, 1),
    ("Cow Milk (Full Cream)", "Milk & Cream", "Dairy", "Litre", 60, 1),
    ("Buffalo Milk", "Milk & Cream", "Dairy", "Litre", 70, 1),
    ("Fresh Curd", "Dairy Products", "Dairy", "Kg", 80, 1),
    ("Farm Paneer", "Dairy Products", "Dairy", "Kg", 300, 1),
    ("Buttermilk", "Dairy Products", "Dairy", "Litre", 40, 1),
    ("Pure Ghee", "Dairy Products", "Dairy", "Litre", 600, 1),
    ("Farm Cheese", "Dairy Products", "Dairy", "Kg", 350, 0),
    ("Flavored Milk (Rose)", "Milk & Cream", "Dairy", "Litre", 50, 0),
    ("Brown Rice", "Grain Products", "Grain", "Kg", 80, 1),
    ("Basmati Rice", "Grain Products", "Grain", "Kg", 120, 0),
    ("Whole Wheat Flour", "Grain Products", "Grain", "Kg", 35, 0),
    ("Toor Dal", "Pulses & Lentils", "Pulse", "Kg", 120, 0),
    ("Moong Dal (Split)", "Pulses & Lentils", "Pulse", "Kg", 110, 1),
    ("Chana Dal", "Pulses & Lentils", "Pulse", "Kg", 90, 0),
    ("Steel Cut Oats", "Grain Products", "Grain", "Kg", 150, 1),
    ("Ragi Flour", "Grain Products", "Grain", "Kg", 70, 1),
    ("Turmeric Powder", "Herbs & Spices", "Spice", "Kg", 250, 1),
    ("Red Chilli Powder", "Herbs & Spices", "Spice", "Kg", 300, 1),
    ("Cumin Seeds (Jeera)", "Herbs & Spices", "Spice", "Kg", 350, 1),
    ("Coriander Powder", "Herbs & Spices", "Spice", "Kg", 200, 1),
    ("Garam Masala", "Herbs & Spices", "Spice", "Kg", 400, 1),
    ("Mixed Herbs (Organic)", "Herbs & Spices", "Herb", "Packet", 50, 1),
    ("Organic Honey", "Herbs & Spices", "Other", "Kg", 500, 1),
    ("Farm Fresh Eggs", "Dairy Products", "Other", "Dozen", 80, 1),
    ("Coconut Water (Fresh)", "Tropical Fruits", "Other", "Litre", 40, 1),
]

SUBSCRIPTION_PLANS = [
    ("Daily Vegetable Box", "Daily", "Weekly", 1200, 1100),
    ("Weekly Fresh Produce Box", "Weekly", "Weekly", 800, 750),
    ("Monthly Organic Family Pack", "Monthly", "Monthly", 3500, 3200),
    ("Dairy Essentials Plan", "Weekly", "Weekly", 500, 450),
    ("Fruits Subscription Plan", "Weekly", "Weekly", 600, 550),
    ("Green Salad Special", "Weekly", "Weekly", 400, 370),
    ("Gourmet Vegetable Box", "Weekly", "Weekly", 1000, 950),
    ("Monthly Grain & Pulse Pack", "Monthly", "Monthly", 1500, 1400),
    ("Weekly Herb & Spice Box", "Weekly", "Weekly", 350, 320),
    ("Premium Organic Combo", "Monthly", "Monthly", 5000, 4600),
]

DELIVERY_ZONES = [
    ("Zone A - Downtown", "Mumbai", "400001", "400010", 30, 200),
    ("Zone B - Suburban North", "Mumbai", "400050", "400080", 40, 300),
    ("Zone C - Central", "Delhi", "110001", "110020", 30, 200),
    ("Zone D - South Delhi", "Delhi", "110030", "110050", 35, 250),
    ("Zone E - Bangalore East", "Bangalore", "560001", "560020", 30, 200),
    ("Zone F - Bangalore West", "Bangalore", "560030", "560060", 35, 250),
    ("Zone G - Hyderabad Central", "Hyderabad", "500001", "500020", 25, 200),
    ("Zone H - Pune City", "Pune", "411001", "411020", 30, 200),
    ("Zone I - Chennai Central", "Chennai", "600001", "600020", 25, 200),
    ("Zone J - Ahmedabad", "Ahmedabad", "380001", "380015", 30, 200),
]

ORDER_STATUSES = ["Draft", "Confirmed", "Processing", "Out for Delivery", "Delivered", "Cancelled"]
SUBSCRIPTION_STATUSES = ["Draft", "Active", "Paused", "Cancelled", "Expired"]
DELIVERY_SCHEDULE_STATUSES = ["Scheduled", "Confirmed", "Out for Delivery", "Delivered", "Cancelled", "Failed"]
PAYMENT_STATUSES = ["Pending", "Completed", "Failed", "Refunded", "Cancelled"]
PAYMENT_MODES = ["UPI", "Card", "Cash on Delivery", "Wallet", "QR Code"]

DELIVERY_TIME_SLOTS = ["6 AM - 8 AM", "8 AM - 10 AM", "10 AM - 12 PM", "4 PM - 6 PM", "6 PM - 8 PM"]


# ──────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────

def log(msg, emoji="📦"):
    print(f"{emoji} {msg}")


def random_phone():
    prefixes = ["98", "99", "97", "96", "95", "90", "88", "87", "86", "85", "84", "83", "82", "81", "80", "70", "77", "74", "73"]
    return f"+91 {random.choice(prefixes)}{random.randint(10000000, 99999999)}"


def random_email(first_name, last_name):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "rediffmail.com", "farm2home.local"]
    return f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{random.choice(domains)}"


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def random_address(city_info):
    areas = ["Main Road", "Gandhi Nagar", "Shastri Nagar", "Lake View", "Green Park",
             "Model Colony", "Sector 7", "Phase 2", "Industrial Area", "Smart City Zone"]
    door_no = random.randint(1, 999)
    street = f"{door_no}, {random.choice(areas)}"
    return street, city_info


def safe_insert(doctype, data_dict, check_field=None):
    """Insert a document safely, skipping if it already exists."""
    try:
        doc = frappe.get_doc(data_dict)
        doc.flags.ignore_permissions = True
        doc.insert()
        return doc.name
    except frappe.DuplicateEntryError:
        if check_field:
            name = data_dict.get(check_field)
            existing = frappe.db.exists(doctype, name)
            if existing:
                return existing
        # Try to find by unique field
        for field in ["name", "category_name", "certification_name", "zone_name",
                       "settings_name", "customer_name", "plan_name", "product_name"]:
            val = data_dict.get(field)
            if val and frappe.db.exists(doctype, val):
                return val
        return None
    except Exception as e:
        log(f"  ⚠️ Failed to create {doctype} '{data_dict.get('name', data_dict.get('product_name', '?'))}': {e}", "⚠️")
        return None


def get_or_create_warehouse():
    """Get or create a default Warehouse for inventory."""
    warehouse = frappe.db.exists("Warehouse", "Farm2Home - Main Warehouse")
    if warehouse:
        return warehouse
    
    # Find if any warehouse exists
    existing = frappe.db.get_value("Warehouse", {"is_group": 0}, "name")
    if existing:
        return existing
    
    try:
        doc = frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": "Farm2Home - Main Warehouse",
            "company": frappe.db.get_single_value("Global Defaults", "default_company") or "Your Company",
        })
        doc.flags.ignore_permissions = True
        doc.insert()
        return doc.name
    except Exception as e:
        log(f"  ⚠️ Failed to create warehouse: {e}", "⚠️")
        return None


def create_customer(customer_name, first_name, last_name, phone, email, city_info):
    """Create a standard ERPNext Customer."""
    city, state, pincode = city_info
    customer_type = random.choice(["Individual", "Individual", "Individual", "Company"])
    
    # Find a non-group Customer Group
    non_group_cg = frappe.db.get_value("Customer Group", {"is_group": 0}, "name")
    if not non_group_cg:
        non_group_cg = "Individual"
    
    customer_data = {
        "doctype": "Customer",
        "customer_name": customer_name,
        "customer_type": customer_type,
        "customer_group": non_group_cg,
        "territory": "All Territories",
        "mobile_no": phone,
        "email_id": email,
    }
    
    try:
        existing = frappe.db.exists("Customer", customer_name)
        if existing:
            return existing
        
        doc = frappe.get_doc(customer_data)
        doc.flags.ignore_permissions = True
        doc.insert()
        return doc.name
    except Exception:
        # Try with a unique suffix
        customer_data["customer_name"] = f"{customer_name}-{random.randint(10, 99)}"
        try:
            doc = frappe.get_doc(customer_data)
            doc.flags.ignore_permissions = True
            doc.insert()
            return doc.name
        except Exception as e:
            log(f"  ⚠️ Failed to create Customer: {e}", "⚠️")
            return None


def create_address(customer_name, address_title, street, city_info, is_primary=False, is_shipping=False):
    """Create a standard ERPNext Address linked to a Customer."""
    city, state, pincode = city_info
    address_data = {
        "doctype": "Address",
        "address_title": address_title,
        "address_type": "Shipping" if is_shipping else "Billing",
        "address_line1": street,
        "city": city,
        "state": state,
        "pincode": pincode,
        "country": "India",
        "is_primary_address": 1 if is_primary else 0,
        "is_shipping_address": 1 if is_shipping else 0,
        "links": [{"link_doctype": "Customer", "link_name": customer_name}],
    }
    try:
        doc = frappe.get_doc(address_data)
        doc.flags.ignore_permissions = True
        doc.insert()
        return doc.name
    except Exception:
        return None


# ──────────────────────────────────────────────
# Data Creation Functions
# ──────────────────────────────────────────────

def create_farm_categories():
    log("Creating Farm Categories...", "🏠")
    for name in FARM_CATEGORIES:
        safe_insert("Farm Category", {
            "doctype": "Farm Category",
            "category_name": name,
            "description": f"{name} category for farm classification",
            "is_active": 1,
        }, "category_name")


def create_organic_certifications():
    log("Creating Organic Certifications...", "📜")
    for name, body in CERTIFICATIONS:
        safe_insert("Organic Certification", {
            "doctype": "Organic Certification",
            "certification_name": name,
            "certifying_body": body,
            "description": f"{name} certified by {body}",
            "is_active": 1,
        }, "certification_name")


def create_product_categories():
    log("Creating Product Categories...", "📂")
    # First create parent categories
    parent_cats = {}
    for cat_name, parent in PRODUCT_CATEGORIES:
        if parent not in parent_cats:
            safe_insert("Product Category", {
                "doctype": "Product Category",
                "category_name": parent,
                "category_type": parent,
                "description": f"{parent} category",
                "is_active": 1,
            }, "category_name")
            parent_cats[parent] = parent
    
    for cat_name, parent in PRODUCT_CATEGORIES:
        safe_insert("Product Category", {
            "doctype": "Product Category",
            "category_name": cat_name,
            "parent_category": parent,
            "category_type": parent,
            "description": f"{cat_name} - {parent} subcategory",
            "is_active": 1,
        }, "category_name")


def create_farms():
    log("Creating Farms...", "🏡")
    created = []
    categories = frappe.get_all("Farm Category", pluck="category_name")
    certifications = frappe.get_all("Organic Certification", pluck="certification_name")
    
    for i, name in enumerate(FARM_NAMES):
        city_info = INDIAN_CITIES[i % len(INDIAN_CITIES)]
        city, state, pincode = city_info
        farm_code = f"FC{i+1:03d}"
        is_organic = random.choice([True, True, False])
        category = random.choice(categories) if categories else None
        
        doc = {
            "doctype": "Farm",
            "farm_name": name,
            "farm_code": farm_code,
            "farm_category": category,
            "status": "Active",
            "is_organic": 1 if is_organic else 0,
            "address": f"{random.randint(1, 999)} {name.split()[0]} Road",
            "city": city,
            "state": state,
            "pincode": pincode,
            "country": "India",
            "contact_person": f"{random.choice(FIRST_NAMES_MALE)} {random.choice(LAST_NAMES)}",
            "phone": random_phone(),
            "email": random_email(name.split()[0].lower(), "farm"),
            "description": f"<p>{name} is a {'certified organic' if is_organic else 'premium quality'} farm producing fresh, chemical-free produce. Located in {city}, {state}.</p>",
            "joined_date": random_date(date(2022, 1, 1), date(2024, 6, 1)).isoformat(),
            "total_products": 0,
            "total_orders": 0,
            "total_revenue": 0,
        }
        
        farm_name_saved = safe_insert("Farm", doc, "farm_name")
        if farm_name_saved:
            created.append(farm_name_saved)
            # Add organic certifications (child table)
            if certifications and is_organic:
                try:
                    farm_doc = frappe.get_doc("Farm", farm_name_saved)
                    num_certs = random.randint(1, min(3, len(certifications)))
                    for cert_name in random.sample(certifications, num_certs):
                        cert_doc = frappe.get_doc("Organic Certification", cert_name) if frappe.db.exists("Organic Certification", cert_name) else None
                        farm_doc.append("organic_certifications", {
                            "certification": cert_name,
                            "certification_number": f"CERT-{cert_name[:3].upper()}-{random.randint(10000, 99999)}",
                            "issue_date": random_date(date(2023, 1, 1), date(2024, 1, 1)).isoformat(),
                            "expiry_date": random_date(date(2025, 1, 1), date(2026, 12, 31)).isoformat(),
                            "certifying_body": cert_doc.certifying_body if cert_doc else "Certifying Body",
                        })
                    farm_doc.flags.ignore_permissions = True
                    farm_doc.save()
                except Exception:
                    pass
            log(f"  ✅ Created Farm: {name}")
    
    return created


def create_farmers():
    log("Creating Farmers...", "👨‍🌾")
    created = []
    farms = frappe.get_all("Farm", pluck="name")
    
    for i in range(20):
        gender = random.choice(["male", "male", "male", "female"])
        first_name = random.choice(FIRST_NAMES_MALE if gender == "male" else FIRST_NAMES_FEMALE)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        city_info = random.choice(INDIAN_CITIES)
        city, state, pincode = city_info
        
        doc = {
            "doctype": "Farmer",
            "first_name": first_name,
            "last_name": last_name,
            "status": "Active",
            "phone": random_phone(),
            "email": random_email(first_name, last_name),
            "address": f"{random.randint(1, 999)}, Farm House, {city}",
            "city": city,
            "state": state,
            "pincode": pincode,
            "country": "India",
            "experience_years": random.randint(3, 35),
            "specialization": random.choice(["Vegetable Farming", "Dairy Farming", "Organic Farming", "Fruit Cultivation", "Mixed Farming"]),
            "id_type": random.choice(["Aadhaar", "PAN Card", "Voter ID"]),
            "id_number": f"{random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
            "bank_name": random.choice(["State Bank of India", "HDFC Bank", "ICICI Bank", "Bank of Baroda", "Punjab National Bank"]),
            "account_number": str(random.randint(10000000000, 99999999999)),
            "ifsc_code": f"{random.choice(['SBIN', 'HDFC', 'ICIC', 'BARB', 'PUNB'])}0{random.randint(10000, 99999)}",
            "account_holder_name": full_name,
        }
        
        farmer_name = safe_insert("Farmer", doc)
        if farmer_name:
            created.append(farmer_name)
            # Add associated farms (child table)
            num_farms = random.randint(1, min(3, len(farms)))
            for farm_name in random.sample(farms, num_farms):
                try:
                    farm_doc = frappe.get_doc("Farmer", farmer_name)
                    farm_doc.append("associated_farms", {
                        "farm": farm_name,
                        "role": random.choice(["Owner", "Owner", "Manager", "Partner"]),
                        "since_date": random_date(date(2018, 1, 1), date(2024, 1, 1)).isoformat(),
                    })
                    farm_doc.flags.ignore_permissions = True
                    farm_doc.save()
                except Exception:
                    pass
            
            log(f"  ✅ Created Farmer: {full_name}")
    
    return created


def create_delivery_zones():
    log("Creating Delivery Zones...", "📍")
    created = []
    for name, city, pincode_start, pincode_end, charge, min_order in DELIVERY_ZONES:
        doc = {
            "doctype": "Delivery Zone",
            "zone_name": name,
            "city": city,
            "state": next((s for c, s, p in INDIAN_CITIES if c == city), "Maharashtra"),
            "pincode_start": pincode_start,
            "pincode_end": pincode_end,
            "delivery_charge": charge,
            "minimum_order_amount": min_order,
            "is_active": 1,
        }
        zone = safe_insert("Delivery Zone", doc, "zone_name")
        if zone:
            created.append(zone)
            log(f"  ✅ Created Zone: {name}")
    return created


def create_delivery_agents():
    log("Creating Delivery Agents...", "🚚")
    created = []
    zones = frappe.get_all("Delivery Zone", pluck="name")
    vehicle_types = ["Bike", "Scooter", "Van", "Bicycle"]
    
    for i in range(20):
        first_name = random.choice(FIRST_NAMES_MALE)
        last_name = random.choice(LAST_NAMES)
        phone_num = random_phone()
        
        doc = {
            "doctype": "Delivery Agent",
            "first_name": first_name,
            "last_name": last_name,
            "status": random.choice(["Active", "Active", "Active", "Active", "On Leave", "Inactive"]),
            "phone": phone_num,
            "email": random_email(first_name, last_name),
            "vehicle_type": random.choice(vehicle_types),
            "vehicle_number": f"{random.choice(['MH', 'DL', 'KA', 'TS', 'P'])}{random.randint(10, 99)}{random.choice(['A', 'B', 'C', 'D', 'E'])}{random.choice(['XY', 'PQ', 'RS', 'MN', 'AB'])}{random.randint(1000, 9999)}",
            "license_number": f"LIC-{random.randint(10000, 99999)}",
            "license_expiry": random_date(date(2025, 1, 1), date(2028, 12, 31)).isoformat(),
        }
        
        agent = safe_insert("Delivery Agent", doc)
        if agent:
            created.append(agent)
            # Assign zones
            if zones:
                num_zones = random.randint(1, min(3, len(zones)))
                try:
                    agent_doc = frappe.get_doc("Delivery Agent", agent)
                    for zone_name in random.sample(zones, num_zones):
                        agent_doc.append("assigned_zones", {
                            "delivery_zone": zone_name,
                            "priority": random.randint(1, 5),
                        })
                    agent_doc.flags.ignore_permissions = True
                    agent_doc.save()
                except Exception:
                    pass
            log(f"  ✅ Created Agent: {first_name} {last_name}")
    return created


def create_products():
    log("Creating Products...", "🥦")
    created = []
    
    for code, (name, cat_name, ptype, unit, price, organic) in enumerate(PRODUCTS, 1):
        # Get category
        category = frappe.db.get_value("Product Category", {"category_name": cat_name}, "name")
        if not category:
            # Try parent category
            for cname, parent in PRODUCT_CATEGORIES:
                if cname == cat_name:
                    category = frappe.db.get_value("Product Category", {"category_name": parent}, "name")
                    break
            if not category:
                category = cat_name
        
        quality_grade = "Premium" if organic else random.choice(["Grade A", "Grade B", "Standard"])
        selling_price = price + random.randint(5, 20)
        
        doc = {
            "doctype": "Product",
            "product_name": name,
            "product_code": f"PC{code:03d}",
            "category": category or cat_name,
            "status": "Active",
            "product_type": ptype,
            "is_organic": 1 if organic else 0,
            "base_price": price,
            "selling_price": selling_price,
            "unit": unit,
            "mrp": price + random.randint(10, 50),
            "stock_quantity": random.randint(100, 5000),
            "reorder_level": random.randint(50, 500),
            "available_for_subscription": 1,
            "available_for_one_time": 1,
            "short_description": f"Fresh {name.lower()}, direct from farm",
            "quality_grade": quality_grade,
            "shelf_life_days": random.choice([3, 5, 7, 10, 15, 30, 60, 90, 180]),
            "storage_instructions": random.choice([
                "Store in cool dry place",
                "Refrigerate at 4°C",
                "Keep refrigerated",
                "Store away from direct sunlight",
                "Ambient storage",
            ]),
        }
        
        product = safe_insert("Product", doc)
        if product:
            created.append(product)
    
    log(f"  ✅ Created {len(created)} Products")
    return created


def create_farm_products():
    log("Creating Farm Products...", "🌾")
    created = []
    farms = frappe.get_all("Farm", pluck="name")
    products = frappe.get_all("Product", pluck="name")
    
    if not farms or not products:
        log("  ⚠️ No farms or products to link!", "⚠️")
        return []
    
    for i in range(50):
        farm = random.choice(farms)
        product = random.choice(products)
        product_doc = frappe.get_doc("Product", product)
        base_price = product_doc.base_price or 40
        farmer_price = base_price - random.randint(5, 15)
        selling_price = base_price + random.randint(10, 30)
        
        doc = {
            "doctype": "Farm Product",
            "farm": farm,
            "product": product,
            "product_name": product_doc.product_name,
            "product_code": product_doc.product_code,
            "status": "Available",
            "season": random.choice(["Summer", "Monsoon", "Winter", "Spring", "All Year"]),
            "is_organic": product_doc.is_organic,
            "farmer_price": max(10, farmer_price),
            "selling_price": selling_price,
            "platform_commission": 10,
            "unit": product_doc.unit or "Kg",
            "quantity_available": random.randint(50, 2000),
            "harvest_date": random_date(date(2024, 1, 1), date(2025, 3, 1)).isoformat(),
            "quality_grade": product_doc.quality_grade or "Grade A",
        }
        
        fp = safe_insert("Farm Product", doc)
        if fp:
            created.append(fp)
    
    log(f"  ✅ Created {len(created)} Farm Products")
    return created


def create_product_inventory():
    log("Creating Product Inventory...", "📦")
    created = []
    products = frappe.get_all("Product", pluck="name")
    warehouse = get_or_create_warehouse()
    
    for product in products:
        qty = random.randint(100, 5000)
        reserved = random.randint(0, int(qty * 0.3))
        
        doc = {
            "doctype": "Product Inventory",
            "product": product,
            "warehouse": warehouse,
            "quantity": qty,
            "reserved_quantity": reserved,
            "available_quantity": qty - reserved,
            "batch_number": f"BATCH-{random.randint(1000, 9999)}",
            "manufacturing_date": random_date(date(2024, 6, 1), date(2025, 1, 1)).isoformat(),
            "expiry_date": random_date(date(2025, 3, 1), date(2025, 12, 31)).isoformat(),
            "status": "Active",
        }
        
        inv = safe_insert("Product Inventory", doc)
        if inv:
            created.append(inv)
    
    log(f"  ✅ Created {len(created)} Product Inventory records")
    return created


def create_customers():
    log("Creating Customers...", "👥")
    created = []
    customer_data_list = []
    
    for i in range(30):
        gender = random.choice(["male", "male", "female", "female"])
        first_name = random.choice(FIRST_NAMES_MALE if gender == "male" else FIRST_NAMES_FEMALE)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        city_info = random.choice(INDIAN_CITIES)
        phone = random_phone()
        email = random_email(first_name, last_name)
        
        customer = create_customer(full_name, first_name, last_name, phone, email, city_info)
        if customer:
            created.append(customer)
            customer_data_list.append((customer, full_name, city_info))
            log(f"  ✅ Created Customer: {full_name}")
    
    return created, customer_data_list


def create_customer_addresses(customer_data_list):
    """Create 50 addresses for customers."""
    log("Creating Customer Addresses...", "🏠")
    created = []
    
    for i in range(50):
        if not customer_data_list:
            break
        customer, customer_display_name, city_info = random.choice(customer_data_list)
        street, _ = random_address(city_info)
        is_primary = i == 0  # First address is primary
        is_shipping = random.random() > 0.3
        
        address = create_address(
            customer_name=customer,
            address_title=f"{customer_display_name.split()[0]}'s {'Home' if random.random() > 0.5 else 'Office'}",
            street=street,
            city_info=city_info,
            is_primary=is_primary,
            is_shipping=is_shipping,
        )
        if address:
            created.append(address)
    
    log(f"  ✅ Created {len(created)} Customer Addresses")
    return created


def create_subscription_plans():
    log("Creating Subscription Plans...", "📋")
    created = []
    products = frappe.get_all("Product", pluck="name")
    
    for name, delivery_freq, bill_freq, base_price, final_price in SUBSCRIPTION_PLANS:
        plan_code = f"SP-{name[:3].upper()}{random.randint(100, 999)}"
        
        doc = {
            "doctype": "Subscription Plan",
            "plan_name": name,
            "plan_code": plan_code,
            "plan_type": "Weekly" if "Weekly" in delivery_freq or "Daily" in delivery_freq else "Monthly",
            "status": "Active",
            "is_active": 1,
            "base_price": base_price,
            "discount_amount": base_price - final_price,
            "billing_frequency": bill_freq,
            "delivery_frequency": delivery_freq,
            "description": f"<p>Our {name.lower()} plan delivers fresh farm produce right to your doorstep. Priced at just ₹{final_price}/- per {bill_freq.lower()}.</p>",
        }
        
        plan = safe_insert("Subscription Plan", doc)
        if plan:
            created.append(plan)
            # Add some products to the plan (child table)
            try:
                plan_doc = frappe.get_doc("Subscription Plan", plan)
                num_products = random.randint(3, 8)
                for product in random.sample(products, min(num_products, len(products))):
                    prod_doc = frappe.get_doc("Product", product)
                    plan_doc.append("subscription_products", {
                        "product": product,
                        "quantity": random.randint(1, 5),
                        "unit": prod_doc.unit or "Kg",
                        "price": prod_doc.selling_price or 50,
                    })
                plan_doc.flags.ignore_permissions = True
                plan_doc.save()
            except Exception:
                pass
            log(f"  ✅ Created Plan: {name}")
    
    return created


def create_subscriptions():
    log("Creating Subscriptions...", "📝")
    created = []
    customers = frappe.get_all("Customer", pluck="name")
    plans = frappe.get_all("Subscription Plan", pluck="name")
    farms = frappe.get_all("Farm", pluck="name")
    zones = frappe.get_all("Delivery Zone", pluck="name")
    
    if not all([customers, plans]):
        log("  ⚠️ Need customers and plans first!", "⚠️")
        return []
    
    for i in range(50):
        customer = random.choice(customers)
        plan = random.choice(plans)
        farm = random.choice(farms) if farms else None
        zone = random.choice(zones) if zones else None
        
        start_date = random_date(date(2024, 1, 1), date(2024, 12, 1))
        end_date = start_date + timedelta(days=random.choice([30, 60, 90, 180, 365]))
        status = random.choice(["Active", "Active", "Active", "Active", "Paused", "Cancelled", "Expired", "Draft"])
        
        plan_doc = frappe.get_doc("Subscription Plan", plan) if isinstance(plan, str) and frappe.db.exists("Subscription Plan", plan) else None
        sub_amount = plan_doc.base_price if plan_doc else random.randint(300, 3000)
        total_amount = sub_amount - (sub_amount * 0.05)
        
        doc = {
            "doctype": "Subscription",
            "customer": customer,
            "subscription_plan": plan,
            "status": "Draft",  # Always start as Draft to satisfy workflow
            "subscription_type": random.choice(["Weekly", "Weekly", "Monthly", "Monthly", "Custom"]),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "farm": farm,
            "delivery_zone": zone,
            "delivery_time_slot": random.choice(DELIVERY_TIME_SLOTS),
            "delivery_day": random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Daily"]),
            "billing_frequency": random.choice(["Weekly", "Monthly", "Monthly"]),
            "subscription_amount": sub_amount,
            "discount_applied": sub_amount * 0.05,
            "total_amount": total_amount,
            "paid_amount": total_amount if status == "Active" else 0,
            "balance_amount": 0 if status == "Active" else total_amount,
            "payment_mode": random.choice(PAYMENT_MODES),
            "is_paused": 1 if status == "Paused" else 0,
            "next_delivery_date": (start_date + timedelta(days=7)).isoformat() if status == "Active" else None,
            "last_delivery_date": start_date.isoformat(),
            "total_deliveries": random.randint(1, 20),
            "total_payments": sub_amount * random.randint(1, 6),
        }
        
        sub = safe_insert("Subscription", doc)
        if sub:
            # Now update status via db_set to bypass workflow validation
            if status != "Draft":
                try:
                    sub_doc = frappe.get_doc("Subscription", sub)
                    sub_doc.db_set("status", status, update_modified=False)
                    sub_doc.db_set("docstatus", 1 if status == "Active" else 0, update_modified=False)
                except Exception:
                    pass
            created.append(sub)
    
    log(f"  ✅ Created {len(created)} Subscriptions")
    return created


def create_orders():
    log("Creating Orders...", "🧾")
    created = []
    customers = frappe.get_all("Customer", pluck="name")
    farms = frappe.get_all("Farm", pluck="name")
    products = frappe.get_all("Product", pluck="name")
    agents = frappe.get_all("Delivery Agent", pluck="name")
    zones = frappe.get_all("Delivery Zone", pluck="name")
    
    if not customers or not products:
        log("  ⚠️ Need customers and products first!", "⚠️")
        return []
    
    for i in range(100):
        customer = random.choice(customers)
        farm = random.choice(farms) if farms else None
        order_date = random_date(date(2024, 1, 1), date(2025, 3, 1))
        
        # Generate order items
        num_items = random.randint(1, 6)
        selected_products = random.sample(products, min(num_items, len(products)))
        items = []
        subtotal = 0
        
        for j, product in enumerate(selected_products):
            prod_doc = frappe.get_doc("Product", product) if isinstance(product, str) and frappe.db.exists("Product", product) else None
            rate = prod_doc.selling_price if prod_doc else random.randint(30, 400)
            qty = random.choice([0.5, 1, 2, 3, 5])
            amount = rate * qty
            subtotal += amount
            items.append({
                "product": product,
                "quantity": qty,
                "unit": prod_doc.unit if prod_doc else "Kg",
                "rate": rate,
                "amount": amount,
            })
        
        delivery_charge = random.choice([0, 30, 40, 50])
        tax = subtotal * 0.05
        discount = subtotal * random.choice([0, 0, 0.05, 0.1])
        grand_total = subtotal + tax + delivery_charge - discount
        
        # Assign weighted statuses
        target_status = random.choices(
            ORDER_STATUSES,
            weights=[5, 15, 10, 10, 40, 20],  # More Delivered and Confirmed
            k=1
        )[0]
        
        doc = {
            "doctype": "Order",
            "customer": customer,
            "order_type": random.choice(["One-time", "One-time", "One-time", "Subscription"]),
            "status": "Draft",  # Always start as Draft to satisfy workflow
            "order_date": order_date.isoformat(),
            "delivery_date": (order_date + timedelta(days=random.randint(1, 5))).isoformat(),
            "farm": farm,
            "order_items": items,
            "subtotal": subtotal,
            "tax_amount": tax,
            "delivery_charge": delivery_charge,
            "discount_amount": discount,
            "grand_total": grand_total,
            "paid_amount": grand_total if target_status == "Delivered" else grand_total * 0.5 if target_status == "Confirmed" else 0,
            "balance_amount": 0 if target_status == "Delivered" else grand_total,
            "delivery_zone": random.choice(zones) if zones else None,
            "delivery_time_slot": random.choice(DELIVERY_TIME_SLOTS),
            "delivery_agent": random.choice(agents) if agents and target_status != "Draft" else None,
            "payment_mode": random.choice(PAYMENT_MODES),
            "payment_status": "Paid" if target_status == "Delivered" else "Pending" if target_status == "Draft" else "Partially Paid",
        }
        
        order = safe_insert("Order", doc)
        if order:
            # Update status via db_set to bypass workflow validation
            if target_status != "Draft":
                try:
                    order_doc = frappe.get_doc("Order", order)
                    order_doc.db_set("status", target_status, update_modified=False)
                    order_doc.db_set("docstatus", 1 if target_status in ("Confirmed", "Delivered", "Out for Delivery", "Processing") else 0, update_modified=False)
                except Exception:
                    pass
            created.append(order)
    
    log(f"  ✅ Created {len(created)} Orders")
    return created


def create_delivery_routes():
    log("Creating Delivery Routes...", "🗺️")
    created = []
    zones = frappe.get_all("Delivery Zone", pluck="name")
    agents = frappe.get_all("Delivery Agent", pluck="name")
    
    for i in range(20):
        zone = random.choice(zones) if zones else None
        agent = random.choice(agents) if agents else None
        route_date = random_date(date(2025, 1, 1), date(2025, 3, 15))
        
        doc = {
            "doctype": "Delivery Route",
            "route_name": f"Route {chr(65+i)} - {zone or 'General'}",
            "delivery_zone": zone,
            "delivery_agent": agent,
            "status": random.choice(["Planned", "Planned", "Completed", "Completed", "In Progress", "Cancelled"]),
            "route_date": route_date.isoformat(),
            "vehicle_number": f"{random.choice(['MH', 'DL', 'KA'])}{random.randint(10, 99)}{random.choice(['A', 'B'])}{random.choice(['XY', 'PQ'])}{random.randint(1000, 9999)}",
            "total_stops": random.randint(5, 20),
            "estimated_distance_km": round(random.uniform(15, 60), 1),
            "estimated_duration_min": random.randint(60, 240),
            "actual_distance_km": round(random.uniform(14, 58), 1),
        }
        
        route = safe_insert("Delivery Route", doc)
        if route:
            created.append(route)
    
    log(f"  ✅ Created {len(created)} Delivery Routes")
    return created


def create_delivery_schedules():
    log("Creating Delivery Schedules...", "📅")
    created = []
    customers = frappe.get_all("Customer", pluck="name")
    orders = frappe.get_all("Order", pluck="name")
    subscriptions = frappe.get_all("Subscription", pluck="name")
    zones = frappe.get_all("Delivery Zone", pluck="name")
    agents = frappe.get_all("Delivery Agent", pluck="name")
    products = frappe.get_all("Product", pluck="name")
    
    if not customers:
        return []
    
    # Temporarily disable notifications that fire on Delivery Schedule events
    # to avoid ModuleNotFoundError (no Python module exists for the notification yet)
    notif_disabled = []
    for notif_name in frappe.get_all("Notification",
        filters={"document_type": "Delivery Schedule", "enabled": 1}, pluck="name"):
        notif_doc = frappe.get_doc("Notification", notif_name)
        notif_doc.db_set("enabled", 0)
        notif_disabled.append(notif_name)
    frappe.db.commit()
    
    try:
        for i in range(100):
            customer = random.choice(customers)
            order = random.choice(orders) if orders and random.random() > 0.5 else None
            sub = random.choice(subscriptions) if subscriptions and random.random() > 0.5 else None
            
            status = random.choice(DELIVERY_SCHEDULE_STATUSES)
            delivery_date = random_date(date(2025, 1, 10), date(2025, 3, 10))
            
            # Create some delivery items (child table)
            num_items = random.randint(1, 4)
            items = []
            for product in random.sample(products, min(num_items, len(products))):
                prod_doc = frappe.get_doc("Product", product) if isinstance(product, str) and frappe.db.exists("Product", product) else None
                qty = random.choice([1, 2, 3, 5])
                delivered = qty if status == "Delivered" else 0
                items.append({
                    "product": product,
                    "product_name": prod_doc.product_name if prod_doc else "Product",
                    "quantity": qty,
                    "unit": prod_doc.unit if prod_doc else "Kg",
                    "delivered_quantity": delivered,
                    "status": "Delivered" if status == "Delivered" else "Pending",
                })
            
            doc = {
                "doctype": "Delivery Schedule",
                "customer": customer,
                "order": order,
                "subscription": sub,
                "status": status,
                "delivery_date": delivery_date.isoformat(),
                "delivery_time_slot": random.choice(DELIVERY_TIME_SLOTS),
                "delivery_zone": random.choice(zones) if zones else None,
                "delivery_agent": random.choice(agents) if agents and status != "Scheduled" else None,
                "tracking_number": f"TRK{random.randint(100000, 999999)}",
                "otp_verification": 1,
                "delivery_otp": str(random.randint(1000, 9999)),
                "actual_delivery_time": delivery_date.isoformat() + " 10:30:00" if status == "Delivered" else None,
                "delivery_confirmation": "Confirmed" if status == "Delivered" else "Pending",
                "delivery_items": items,
            }
            
            ds = safe_insert("Delivery Schedule", doc)
            if ds:
                created.append(ds)
    finally:
        # Re-enable notifications
        for notif_name in notif_disabled:
            notif_doc = frappe.get_doc("Notification", notif_name)
            notif_doc.db_set("enabled", 1)
        frappe.db.commit()
    
    log(f"  ✅ Created {len(created)} Delivery Schedules")
    return created


def create_payment_transactions():
    log("Creating Payment Transactions...", "💳")
    created = []
    customers = frappe.get_all("Customer", pluck="name")
    orders = frappe.get_all("Order", pluck="name")
    subscriptions = frappe.get_all("Subscription", pluck="name")
    
    if not customers:
        return []
    
    for i in range(100):
        customer = random.choice(customers)
        order = random.choice(orders) if orders and random.random() > 0.4 else None
        sub = random.choice(subscriptions) if subscriptions and random.random() > 0.4 else None
        
        amount = random.randint(100, 2000)
        status = random.choices(PAYMENT_STATUSES, weights=[10, 60, 10, 5, 15], k=1)[0]
        payment_mode = random.choice(PAYMENT_MODES)
        payment_date = random_date(date(2024, 6, 1), date(2025, 3, 1))
        
        doc = {
            "doctype": "Payment Transaction",
            "customer": customer,
            "order": order,
            "subscription": sub,
            "status": status,
            "payment_date": payment_date.isoformat(),
            "payment_mode": payment_mode,
            "amount": amount,
            "transaction_fee": round(amount * 0.02, 2),
            "currency": "INR",
            "transaction_id": f"TXN{random.randint(100000, 999999)}",
            "reference_number": f"REF{random.randint(100000, 999999)}",
            "upi_id": f"{customer.lower().replace(' ', '')[:8]}@upi" if payment_mode == "UPI" else None,
        }
        
        pay = safe_insert("Payment Transaction", doc)
        if pay:
            created.append(pay)
    
    log(f"  ✅ Created {len(created)} Payment Transactions")
    return created


def create_subscription_billings():
    log("Creating Subscription Billings...", "💰")
    created = []
    subscriptions = frappe.get_all("Subscription", pluck="name")
    
    if not subscriptions:
        return []
    
    for sub in subscriptions:
        sub_doc = frappe.get_doc("Subscription", sub) if isinstance(sub, str) and frappe.db.exists("Subscription", sub) else None
        if not sub_doc:
            continue
        
        num_bills = random.randint(1, 6)
        for j in range(num_bills):
            period_start = random_date(date(2024, 1, 1), date(2025, 1, 1))
            period_end = period_start + timedelta(days=30)
            amount = sub_doc.subscription_amount or random.randint(300, 2000)
            
            doc = {
                "doctype": "Subscription Billing",
                "subscription": sub,
                "customer": sub_doc.customer,
                "status": random.choice(["Generated", "Sent", "Paid", "Paid", "Paid"]),
                "billing_period_start": period_start.isoformat(),
                "billing_period_end": period_end.isoformat(),
                "subscription_amount": amount,
                "additional_charges": random.choice([0, 30, 50]),
                "discount": random.choice([0, 0, amount * 0.05]),
                "total_amount": amount + random.choice([0, 30, 50]),
                "paid_amount": amount if random.random() > 0.2 else 0,
                "balance_amount": 0,
                "payment_status": random.choice(["Paid", "Paid", "Paid", "Pending"]),
                "due_date": period_end.isoformat(),
            }
            
            bill = safe_insert("Subscription Billing", doc)
            if bill:
                created.append(bill)
    
    log(f"  ✅ Created {len(created)} Subscription Billings")
    return created


def create_customer_reviews():
    log("Creating Customer Reviews...", "⭐")
    created = []
    customers = frappe.get_all("Customer", pluck="name")
    products = frappe.get_all("Product", pluck="name")
    farms = frappe.get_all("Farm", pluck="name")
    orders = frappe.get_all("Order", pluck="name")
    
    if not customers:
        return []
    
    review_titles = [
        "Excellent quality!",
        "Very fresh produce",
        "Good value for money",
        "Farm fresh delivery",
        "Loved the taste!",
        "Highly recommended",
        "Great service",
        "Superior quality",
        "Fresh and organic",
        "Will order again",
        "Amazing farm products",
        "Good packaging",
        "Timely delivery",
        "Freshness guaranteed",
        "Best in town",
    ]
    
    review_texts = [
        "The produce was incredibly fresh and well-packaged. Definitely ordering again!",
        "Great quality farm products. The vegetables were crisp and full of flavor.",
        "Very satisfied with the quality. The delivery was on time and everything was fresh.",
        "Excellent farm-to-table experience. The freshness of the products is unmatched.",
        "Good quality products at reasonable prices. Highly recommend for organic produce.",
        "The vegetables were so fresh, they looked like they were just picked from the farm.",
        "Loved the taste and quality. Farm2Home never disappoints!",
        "Prompt delivery and excellent product quality. Very happy with the service.",
        "The organic produce is truly farm fresh. You can taste the difference.",
        "Reliable service with consistently good quality. A regular customer now.",
    ]
    
    for i in range(40):
        customer = random.choice(customers)
        product = random.choice(products) if products else None
        farm = random.choice(farms) if farms else None
        order = random.choice(orders) if orders else None
        rating = random.randint(3, 5)  # Mostly positive reviews
        
        doc = {
            "doctype": "Customer Review",
            "customer": customer,
            "farm": farm,
            "product": product,
            "rating": rating,
            "review_date": random_date(date(2024, 6, 1), date(2025, 3, 1)).isoformat(),
            "order": order,
            "review_title": random.choice(review_titles),
            "review_text": f"<p>{random.choice(review_texts)}</p>",
            "is_approved": 1 if rating >= 3 else random.choice([0, 1]),
            "is_featured": 1 if rating == 5 and random.random() > 0.7 else 0,
        }
        
        review = safe_insert("Customer Review", doc)
        if review:
            created.append(review)
    
    log(f"  ✅ Created {len(created)} Customer Reviews")
    return created


def create_customer_wallets():
    log("Creating Customer Wallets...", "👛")
    created = []
    customers = frappe.get_all("Customer", pluck="name")
    
    for customer in customers:
        total_credited = random.randint(500, 10000)
        total_debited = random.randint(200, total_credited)
        balance = total_credited - total_debited
        
        doc = {
            "doctype": "Customer Wallet",
            "customer": customer,
            "balance": balance,
            "total_credited": total_credited,
            "total_debited": total_debited,
        }
        
        wallet = safe_insert("Customer Wallet", doc)
        if wallet:
            created.append(wallet)
            # Add wallet transactions (child table)
            try:
                wallet_doc = frappe.get_doc("Customer Wallet", wallet)
                num_txns = random.randint(2, 8)
                for t in range(num_txns):
                    txn_amount = random.randint(50, 2000)
                    wallet_doc.append("transactions", {
                        "transaction_type": random.choice(["Credit", "Credit", "Debit"]),
                        "amount": txn_amount,
                        "reference": f"TXN-{random.randint(1000, 9999)}",
                        "date": random_date(date(2024, 6, 1), date(2025, 3, 1)).isoformat(),
                        "notes": random.choice(["Order payment", "Wallet top-up", "Refund", "Subscription payment"]),
                    })
                wallet_doc.flags.ignore_permissions = True
                wallet_doc.save()
            except Exception:
                pass
    
    log(f"  ✅ Created {len(created)} Customer Wallets")
    return created


def create_wishlists():
    log("Creating Wishlists...", "❤️")
    created = []
    customers = frappe.get_all("Customer", pluck="name")
    products = frappe.get_all("Product", pluck="name")
    
    for customer in customers:
        num_items = random.randint(1, 5)
        items = []
        for product in random.sample(products, min(num_items, len(products))):
            prod_doc = frappe.get_doc("Product", product) if isinstance(product, str) and frappe.db.exists("Product", product) else None
            items.append({
                "product": product,
                "added_date": random_date(date(2024, 6, 1), date(2025, 3, 1)).isoformat(),
                "notes": random.choice(["", "Regular purchase", "Favorite", "Try this"]),
            })
        
        doc = {
            "doctype": "Wishlist",
            "customer": customer,
            "wishlist_items": items,
        }
        
        wishlist = safe_insert("Wishlist", doc)
        if wishlist:
            created.append(wishlist)
    
    log(f"  ✅ Created {len(created)} Wishlists")
    return created


def create_quality_inspections():
    log("Creating Quality Inspections...", "🔍")
    created = []
    products = frappe.get_all("Product", pluck="name")
    farms = frappe.get_all("Farm", pluck="name")
    
    for i in range(min(30, len(products) * 2)):
        product = random.choice(products) if products else None
        farm = random.choice(farms) if farms else None
        if not product:
            continue
        
        overall_grade = random.choice(["Grade A", "Grade A", "Grade B", "Premium", "Standard"])
        result = "Pass" if overall_grade != "Rejected" else "Fail"
        
        doc = {
            "doctype": "Quality Inspection",
            "product": product,
            "farm": farm,
            "status": "Approved" if result == "Pass" else "Rejected",
            "inspection_date": random_date(date(2024, 6, 1), date(2025, 3, 1)).isoformat(),
            "appearance": random.randint(3, 5),
            "freshness": random.randint(3, 5),
            "size_uniformity": random.randint(3, 5),
            "pesticide_residue": random.choice(["None", "None", "Within Limits"]),
            "moisture_content": random.randint(10, 30),
            "overall_grade": overall_grade,
            "organic_verified": 1 if random.random() > 0.5 else 0,
            "result": result,
            "remarks": f"<p>Product inspected and {result.lower()}ed quality standards. Grade: {overall_grade}.</p>",
        }
        
        qi = safe_insert("Quality Inspection", doc)
        if qi:
            created.append(qi)
    
    log(f"  ✅ Created {len(created)} Quality Inspections")
    return created


# ──────────────────────────────────────────────
# Main Entry Point
# ──────────────────────────────────────────────

def create_demo_data():
    """Main entry point. Run via:
    bench --site sudhakar1.site execute farm2home.farm_to_home.demo_data.create_demo_data
    """
    log("=" * 60, "🚀")
    log("Farm2Home Demo Data Generator", "🚀")
    log("=" * 60, "🚀")
    
    # Step 1: Base reference data (no dependencies)
    create_farm_categories()
    create_organic_certifications()
    create_product_categories()
    
    # Step 2: Core entities
    create_farms()
    create_farmers()
    create_delivery_zones()
    create_delivery_agents()
    
    # Step 3: Products & Inventory
    create_products()
    create_farm_products()
    create_product_inventory()
    
    # Step 4: Customers and Addresses (standard ERPNext)
    _, customer_data_list = create_customers()
    create_customer_addresses(customer_data_list)
    
    # Step 5: Subscriptions
    create_subscription_plans()
    create_subscriptions()
    
    # Step 6: Orders & Deliveries
    create_orders()
    create_delivery_routes()
    create_delivery_schedules()
    
    # Step 7: Payments & Billing
    create_payment_transactions()
    create_subscription_billings()
    
    # Step 8: Customer Engagement
    create_customer_reviews()
    create_customer_wallets()
    create_wishlists()
    
    # Step 9: Quality
    create_quality_inspections()
    
    log("=" * 60, "🎉")
    log("Demo data generation complete!", "🎉")
    log("=" * 60, "🎉")
    
    # Summary
    log("\n📊 Summary:", "📊")
    for doctype in [
        "Farm Category", "Organic Certification", "Product Category",
        "Farm", "Farmer", "Delivery Zone", "Delivery Agent",
        "Product", "Farm Product", "Product Inventory",
        "Customer", "Subscription Plan", "Subscription",
        "Order", "Delivery Route", "Delivery Schedule",
        "Payment Transaction", "Subscription Billing",
        "Customer Review", "Customer Wallet", "Wishlist", "Quality Inspection",
    ]:
        count = frappe.db.count(doctype)
        log(f"  {doctype}: {count}", "📊")


def cleanup_demo_data():
    """Delete all demo data created by this script.
    Run via:
        bench --site sudhakar1.site execute farm2home.farm_to_home.demo_data.cleanup_demo_data
    """
    log("=" * 60, "🧹")
    log("Cleaning up all Farm2Home demo data...", "🧹")
    log("=" * 60, "🧹")
    
    # Order matters: child-table-dependent first, then parents
    delete_order = [
        # Child-table-dependent first
        "Delivery Schedule",
        "Customer Review",
        "Customer Wallet",
        "Wishlist",
        "Farm Product",
        "Product Inventory",
        "Quality Inspection",
        "Payment Transaction",
        "Subscription Billing",
        # Core transactional
        "Order",
        "Subscription",
        "Delivery Route",
        # Customers & Addresses
        "Address",
        "Customer",
        # Product/Subscription data
        "Product",
        "Subscription Plan",
        "Farm Category",
        "Product Category",
        "Organic Certification",
        # Agents & Zones
        "Delivery Agent",
        "Delivery Zone",
        # Farm data last (farmers reference farms)
        "Farmer",
        "Farm",
    ]
    
    total = 0
    for dt in delete_order:
        try:
            count = frappe.db.count(dt)
            if count > 0:
                frappe.db.delete(dt, {})
                total += count
                log(f"  ✅ Deleted {count} {dt}(s)", "🧹")
        except Exception as e:
            try:
                table_name = f"tab{dt}"
                frappe.db.sql(f"DELETE FROM `{table_name}`")
                log(f"  ✅ SQL-deleted {dt}", "🧹")
            except Exception as e2:
                log(f"  ⚠️ Could not delete {dt}: {e2}", "⚠️")
    
    # Also reset autoname series counters
    try:
        frappe.db.delete("Series", {"name": ["like", "FARM-%"]})
        frappe.db.delete("Series", {"name": ["like", "PROD-%"]})
        frappe.db.delete("Series", {"name": ["like", "REV-%"]})
        frappe.db.delete("Series", {"name": ["like", "SUB-%"]})
        frappe.db.delete("Series", {"name": ["like", "ORD-%"]})
        log(f"  ✅ Reset autoname series counters", "🧹")
    except Exception:
        pass
    
    frappe.db.commit()
    frappe.clear_cache()
    
    log("=" * 60, "🧹")
    log(f"Cleanup complete! Deleted {total} records.", "🧹")
    log("=" * 60, "🧹")


if __name__ == "__main__":
    create_demo_data()
