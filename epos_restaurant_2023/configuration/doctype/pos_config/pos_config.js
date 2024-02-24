// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("POS Config", {
	onload(frm) {
        frm.set_query("tip_account_code", function() {
            return {
                filters: [["is_group","=",0]]
            }
        });
        frm.set_query("account_code","payment_type", function() {
            return {
                filters: [
                    ["Account Code","is_group", "=", 0]
                ]
            }
        });
       
	},
});
