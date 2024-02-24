// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("POS Reservation", {
	refresh(frm) { 
        if(frm.doc.__islocal){
            frm.doc.reservation_status = "Reserved";
            frm.refresh_field("reservation_status");
            frm.doc.status = "Reserved";
            frm.refresh_field("status");
            set_df_propert(frm,"confirmed","hidden",1);
            set_query(frm,"reservation_status",[
                ["POS Reservation Status","reservation_status","=","Reserved"]
            ]); 

          

            // Button action sc
        }else{
             
            if(frm.doc.reservation_status == undefined || frm.doc.reservation_status == ""){
                frm.doc.reservation_status = frm.doc.status;
                frm.refresh_field("status");
            }

            if(frm.doc.reservation_status == "Reserved"){
                set_query(frm,"reservation_status",[
                    ["POS Reservation Status","reservation_status","in","Confirmed,Reserved"]
                ]); 
            }
            else if(frm.doc.reservation_status == "Confirmed"){
                set_query(frm,"reservation_status",[
                    ["POS Reservation Status","reservation_status","in","No Show,Void,Confirmed"]
                ]); 
            }
            else if(frm.doc.reservation_status == "No Show"){
                set_query(frm,"reservation_status",[
                    ["POS Reservation Status","reservation_status","in","No Show,Void"]
                ]); 
            }
            else{
                set_query(frm,"reservation_status",[
                    ["POS Reservation Status","reservation_status","in",`${frm.doc.reservation_status}`]
                ]);  
            }   
            
            //set readonly
            if(frm.doc.reservation_status == "Dine-in" || frm.doc.reservation_status == "Checked Out" || frm.doc.reservation_status == "Void" || frm.doc.reservation_status == "No Show"){
                set_df_propert(frm,"property","read_only",1);
                set_df_propert(frm,"table_id","read_only",1);
                set_df_propert(frm,"total_guest","read_only",1);
                set_df_propert(frm,"reservation_date","read_only",1);
                set_df_propert(frm,"arrival_date","read_only",1);
                set_df_propert(frm,"arrival_time","read_only",1); 
                set_df_propert(frm,"guest","read_only",1);
                set_df_propert(frm,"reservation_product","read_only",1);
                set_df_propert(frm,"reservation_status","read_only",1);
            }
        }
	},
 
    setup(frm) {  
        
    }, 
    
});

function set_query(frm,field_name, filters){	 
    frm.set_query(field_name, function() {
        return {
            filters: filters
        }
    }); 
}

function set_df_propert(frm,field_name,property,property_value){
    frm.set_df_property(field_name,property, property_value);	
    frm.refresh_field(field_name);
}

frappe.ui.form.on('POS Reservation Item', {
	reservation_product_remove: function(frm) {
		updateSumTotal(frm);
    },
	product_code(frm,cdt, cdn) {
		let doc=   locals[cdt][cdn];
		get_product_code(frm,doc);
	},
	price(frm,cdt, cdn) {	
		const row = locals[cdt][cdn];
		if (row.allow_change_price==0 && row.price != row.base_price){
			frappe.msgprint(__("This is not allow to change price"));
			row.price = row.base_price;
		}
		update_reservation_product_amount(frm,row);
		
	},
	quantity(frm,cdt, cdn) {
		let row = locals[cdt][cdn];
		update_reservation_product_amount(frm,row);
	},

	unit(frm,cdt, cdn) {
			let row = locals[cdt][cdn];
			if(row.product_code){ 				
				get_product_price(frm,row).then((v)=>{
					row.price = v;
                    row.regular_price = v;
					update_reservation_product_amount(frm,row)
				});
			}
	},
})

function updateSumTotal(frm) {
    const products =  frm.doc.reservation_product;
    if(products==undefined){
        return false;
    }
    
    frm.set_value('total_amount', products.reduce((n, d) => n + (d.price * d.quantity),0));
    frm.set_value('total_quantity', products.reduce((n, d) => n + d.quantity,0));  

    frm.refresh_field('total_amount'); 
}


let get_product_price = function (frm,doc) {	
	return new Promise(function(resolve, reject) {		
		frappe.call({
			method: "epos_restaurant_2023.inventory.doctype.product.product.get_product_price",
			args: {
				barcode:doc.product_code,
				business_branch:frm.doc.property,
				unit:doc.unit
			},
			callback: function(r){		
				resolve(r.message.price)
			},
			error: function(r) {
				reject("error")
			},
		});	
	});
}

function get_product_code(frm,doc){
    get_product_price(frm,doc).then((v)=>{
        doc.price = v;
        doc.regular_price = v;
        update_reservation_product_amount(frm,doc);        
    });

}

function update_reservation_product_amount(frm,doc){
    doc.total_amount = doc.price * doc.quantity;
    updateSumTotal(frm)
	frm.refresh_field('reservation_product');
}

