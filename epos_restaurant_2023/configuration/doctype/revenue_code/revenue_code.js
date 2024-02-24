// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Revenue Code", {
	onload(frm) {
        frm.set_query("tax_1_account", function() {
            return {
                filters: [
                    ["Account Code","is_group", "=", 0]
                ]
            }
        });
        frm.set_query("tax_2_account", function() {
            return {
                filters: [
                    ["Account Code","is_group", "=", 0]
                ]
            }
        });
        frm.set_query("tax_3_account", function() {
            return {
                filters: [
                    ["Account Code","is_group", "=", 0]
                ]
            }
        });
	},
});
