// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product Category", {
	refresh(frm) {

	},
    setup(frm){
        frm.set_query('parent_product_category', () => {
            return {
                filters: {
                    is_group: 1
                }
            }
        });
    },
});
