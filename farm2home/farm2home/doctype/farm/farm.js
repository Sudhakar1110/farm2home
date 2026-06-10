frappe.ui.form.on('Farm', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View Products'), function() {
                frappe.set_route('List', 'Farm Product', {farm: frm.doc.name});
            }, __('View'));
            
            frm.add_custom_button(__('View Orders'), function() {
                frappe.set_route('List', 'Order', {farm: frm.doc.name});
            }, __('View'));
            
            frm.add_custom_button(__('Update Metrics'), function() {
                frappe.call({
                    method: 'farm2home.farm2home.doctype.farm.farm.update_farm_performance_metrics',
                    callback: function(r) {
                        frm.reload_doc();
                        frappe.show_alert({message: __('Metrics updated'), indicator: 'green'});
                    }
                });
            }, __('Actions'));
        }
    },
    
    farm_code: function(frm) {
        if (frm.doc.farm_code) {
            frm.set_value('farm_code', frm.doc.farm_code.toUpperCase());
        }
    }
});
