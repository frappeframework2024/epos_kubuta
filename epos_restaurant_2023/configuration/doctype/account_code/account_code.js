// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Account Code", {
     
	refresh(frm) {
        frm.set_df_property('field_name', 'fieldtype', 'Data');
        frm.set_query("discount_account", function() {
            return {
                filters: [["is_group","=",0]]
            }
        });
        
        frm.set_query("target_account_code", function() {
            return {
                filters: [["is_group","=",0]]
            }
        });

        frm.set_query("bank_fee_account", function() {
            return {
                filters: [["is_group","=",0]]
            }
        });
        
        frm.set_query("parent_account_code", function() {
            return {
                filters: [["is_group","=",1]]
            }
        });

	},
});
