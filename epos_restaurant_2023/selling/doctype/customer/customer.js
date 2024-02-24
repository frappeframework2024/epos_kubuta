// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", { 
    onload(frm){
        frm.set_df_property('billing_section', 'hidden',is_new()?1:0);
    }
});
