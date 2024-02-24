// Copyright (c) 2024, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer Payment", {
	refresh(frm) {
        frm.set_query("customer", function() {
            return {
                filters: [["balance",">",0]]
            }
        });
	},
    customer(frm){
        frappe.db.get_list('Sale',{
            fields: ['balance', 'name'],
            filters: {
                balance: ['>',0]
            }
        }).then((data)=>{ 
            frm.add_child('payment_invoice', {
                invoice:data.name
            }).then((res)=>{
                frm.refresh_field('items');
            });
            
        })
        
        
    }
});
