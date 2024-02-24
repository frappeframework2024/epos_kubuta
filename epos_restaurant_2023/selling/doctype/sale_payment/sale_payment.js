frappe.ui.form.on("Sale Payment", {
    onload(frm){
        if(frm.doc.__islocal){
            if((frm.doc.pos_reservation||"") !="" ){
                frm.doc.transaction_type = "Payment";
                frm.doc.is_reservation_deposit = 1;
                frm.doc.sale =undefined;
                set_query(frm,"sale",[["Sale","docstatus", "=", 1], ["Sale","from_reservation", "=", frm.doc.pos_reservation], ["Sale","balance", ">=", 0.01]]);                
                set_df_propert(frm,"transaction_type","read_only",1);
                set_df_propert(frm,"sale_information_section","hidden",1);
                set_df_propert(frm,"is_reservation_deposit","hidden",0);
            }else{
                frm.doc.is_reservation_deposit =0;
                set_df_propert(frm,"is_reservation_deposit","hidden",1);
            }
        }else{
            if((frm.doc.pos_reservation||"") !="" ){
                set_query(frm,"sale",[["Sale","docstatus", "=", 1], ["Sale","from_reservation", "=", frm.doc.pos_reservation], ["Sale","balance", ">=", 0.01]]);                
                set_df_propert(frm,"transaction_type","read_only",1);

                if((frm.doc.is_reservation_deposit||0)==1){
                    set_df_propert(frm,"sale","read_only",1);
                    // set_df_propert(frm,"sale_information_section","hidden",0);
                    if((frm.doc.sale||"")==""){
                        //set_df_propert(frm,"sale_information_section","hidden",1);
                    }
                }                
            }else{
                set_df_propert(frm,"reservation_section","hidden",1);                
            }
        }
    },
    setup(frm) {
        set_query(frm,"sale",[["Sale","docstatus", "=", 1], ["Sale","balance", ">=", 0.01]]);
        set_query(frm,"pos_reservation",[["POS Reservation","reservation_status", "not in", "Void"]]);         
    },
    input_amount(frm){
        frm.set_value('payment_amount', frm.doc.input_amount/frm.doc.exchange_rate);
    }
});

function set_df_propert(frm,field_name,property,property_value){
    frm.set_df_property(field_name,property, property_value);	
    frm.refresh_field(field_name);
}


function set_query(frm,doc_field,filters){
    frm.set_query(doc_field, function() {
        return {
            filters: filters
        }
    });
      
}