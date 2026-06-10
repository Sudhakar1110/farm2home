frappe.ui.form.on('Subscription', {
    refresh: function(frm) {
        if (frm.doc.docstatus == 1 && frm.doc.status == 'Active') {
            frm.add_custom_button(__('Pause'), function() {
                frappe.prompt([
                    {fieldname: 'start_date', fieldtype: 'Date', label: 'Pause Start Date', reqd: 1, default: frappe.datetime.get_today()},
                    {fieldname: 'end_date', fieldtype: 'Date', label: 'Pause End Date'},
                    {fieldname: 'reason', fieldtype: 'Small Text', label: 'Reason'}
                ], function(values) {
                    frappe.call({
                        method: 'farm2home.farm2home.doctype.subscription.subscription.pause_subscription',
                        args: {
                            subscription: frm.doc.name,
                            start_date: values.start_date,
                            end_date: values.end_date,
                            reason: values.reason
                        },
                        callback: function(r) {
                            frm.reload_doc();
                            frappe.show_alert({message: r.message, indicator: 'green'});
                        }
                    });
                }, __('Pause Subscription'), __('Pause'));
            }, __('Actions'));
        }
        
        if (frm.doc.status == 'Paused') {
            frm.add_custom_button(__('Resume'), function() {
                frappe.call({
                    method: 'farm2home.farm2home.doctype.subscription.subscription.resume_subscription',
                    args: {subscription: frm.doc.name},
                    callback: function(r) {
                        frm.reload_doc();
                        frappe.show_alert({message: r.message, indicator: 'green'});
                    }
                });
            }, __('Actions'));
        }
    },
    
    subscription_plan: function(frm) {
        if (frm.doc.subscription_plan) {
            frappe.db.get_doc('Subscription Plan', frm.doc.subscription_plan).then(plan => {
                frm.set_value('subscription_amount', plan.final_price);
                frm.set_value('billing_frequency', plan.billing_frequency);
            });
        }
    },
    
    subscription_amount: function(frm) {
        calculate_totals(frm);
    },
    
    discount_applied: function(frm) {
        calculate_totals(frm);
    },
    
    paid_amount: function(frm) {
        calculate_totals(frm);
    }
});

function calculate_totals(frm) {
    let total = (frm.doc.subscription_amount || 0) - (frm.doc.discount_applied || 0);
    let balance = total - (frm.doc.paid_amount || 0);
    frm.set_value('total_amount', total);
    frm.set_value('balance_amount', balance);
}
