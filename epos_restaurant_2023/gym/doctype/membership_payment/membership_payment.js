// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Membership Payment", {
	refresh(frm) {

	},
    onload(frm){
        
    },
    payment_type:function(frm){
        frm.doc.input_amount = (frm.doc.balance||0) * (frm.doc.exchange_rate||1)
        frm.refresh_field("input_amount");
        on_calculate_payment_amount(frm)
    },
    input_amount:function(frm){
        on_calculate_payment_amount(frm)
    }
});

function on_calculate_payment_amount(frm){
    frm.doc.payment_amount =  (frm.doc.input_amount ||0) / (frm.doc.exchange_rate||1);
    frm.refresh_field("payment_amount");    
}
