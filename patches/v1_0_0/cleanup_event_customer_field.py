import frappe


def execute():
    """Remove leftover event_customer field from Customer doctype.

    This field was left behind by a previously uninstalled app (Event Booking Platform)
    and references a non-existing doctype 'Event Customer'. It causes errors when
    opening the Customer form in Frappe Desk.

    Uses multiple approaches to ensure cleanup succeeds even if some records were
    partially deleted by a previous failed migration.
    """
    doctype = "Customer"
    field_name = "event_customer"
    custom_field_name = f"{doctype}-{field_name}"

    # ── Approach 1: Delete via frappe.delete_doc (preferred) ──
    try:
        if frappe.db.exists("Custom Field", custom_field_name):
            frappe.delete_doc("Custom Field", custom_field_name, ignore_permissions=True, force=True)
            frappe.db.commit()
            print(f"✅ Removed Custom Field '{custom_field_name}'")
    except Exception as e:
        print(f"⚠️ delete_doc failed for Custom Field '{custom_field_name}': {e}")

    # ── Approach 2: Direct DB delete (backup in case delete_doc fails) ──
    try:
        deleted = frappe.db.delete("Custom Field", {
            "dt": doctype,
            "fieldname": field_name
        })
        if deleted:
            frappe.db.commit()
            print(f"✅ DB-deleted Custom Field for {doctype}.{field_name}")
    except Exception as e:
        print(f"⚠️ DB delete failed for Custom Field: {e}")

    # ── Clean up Property Setters referencing this field ──
    try:
        ps_names = frappe.get_all("Property Setter",
            filters={"doc_type": doctype, "field_name": field_name},
            pluck="name"
        )
        for ps_name in ps_names:
            try:
                frappe.delete_doc("Property Setter", ps_name, ignore_permissions=True, force=True)
                print(f"✅ Removed Property Setter '{ps_name}'")
            except Exception:
                frappe.db.delete("Property Setter", {"name": ps_name})
                print(f"✅ DB-deleted Property Setter '{ps_name}'")
        if ps_names:
            frappe.db.commit()
    except Exception as e:
        print(f"⚠️ Property Setter cleanup failed: {e}")

    # ── Clean up Client Scripts referencing this field ──
    try:
        cs_names = frappe.get_all("Client Script",
            filters=[
                ["dt", "=", doctype],
                ["script", "like", f"%{field_name}%"]
            ],
            pluck="name"
        )
        for cs_name in cs_names:
            frappe.delete_doc("Client Script", cs_name, ignore_permissions=True, force=True)
            print(f"✅ Removed Client Script '{cs_name}' referencing {field_name}")
        if cs_names:
            frappe.db.commit()
    except Exception as e:
        print(f"⚠️ Client Script cleanup failed: {e}")

    # ── Clean up Server Scripts referencing this doctype ──
    try:
        ss_names = frappe.get_all("Server Script",
            filters={"reference_doctype": "Event Customer"},
            pluck="name"
        )
        for ss_name in ss_names:
            frappe.delete_doc("Server Script", ss_name, ignore_permissions=True, force=True)
            print(f"✅ Removed Server Script '{ss_name}' referencing Event Customer")
        if ss_names:
            frappe.db.commit()
    except Exception as e:
        print(f"⚠️ Server Script cleanup failed: {e}")

    # ── Clean up ANY other leftover event_* fields on ANY doctype ──
    try:
        all_event_fields = frappe.get_all("Custom Field",
            filters={"fieldname": ("like", "event_%")},
            fields=["name", "dt", "fieldname"]
        )
        for cf in all_event_fields:
            try:
                frappe.delete_doc("Custom Field", cf["name"], ignore_permissions=True, force=True)
                print(f"✅ Removed leftover Custom Field '{cf['name']}' from {cf['dt']}")
            except Exception:
                frappe.db.delete("Custom Field", {"name": cf["name"]})
                print(f"✅ DB-deleted leftover Custom Field '{cf['name']}' from {cf['dt']}")
        if all_event_fields:
            frappe.db.commit()
    except Exception as e:
        print(f"⚠️ Broader event_* cleanup failed: {e}")

    # ── Clear cache so Frappe re-evaluates field validity ──
    try:
        frappe.clear_cache(doctype=doctype)
        print(f"✅ Cleared cache for {doctype} doctype")
    except Exception as e:
        print(f"⚠️ Cache clear failed: {e}")

    print("✅ event_customer cleanup complete")
