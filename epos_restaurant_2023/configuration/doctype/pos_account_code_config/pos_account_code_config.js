// Copyright (c) 2024, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("POS Account Code Config", {
	onload(frm) {
        frm.set_query("tax_1_account", function() {
            return {
                filters: [["is_group","=",0]]
            }
        });
        frm.set_query("tax_2_account", function() {
            return {
                filters: [["is_group","=",0]]
            }
        });
        frm.set_query("tax_3_account", function() {
            return {
                filters: [["is_group","=",0]]
            }
        });
        frm.set_query("account_code","pos_revenue_account_codes", function() {
            return {
                filters: [
                    ["Account Code","is_group", "=", 0]
                ]
            }
        });

        frm.set_query("discount_account","pos_revenue_account_codes", function() {
            return {
                filters: [
                    ["Account Code","is_group", "=", 0]
                ]
            }
        });

        frm.set_query("account_code","pos_payment_type_account_codes", function() {
            return {
                filters: [
                    ["Account Code","is_group", "=", 0]
                ]
            }
        });
        frm.set_query("bank_fee_account","pos_payment_type_account_codes", function() {
            return {
                filters: [
                    ["Account Code","is_group", "=", 0]
                ]
            }
        });
	},
});
