// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Membership Options", {
	refresh(frm) {
        on_tracking_limited_changed(frm);       
        on_membership_type_changed(frm);
        on_duration_type_changed(frm);
        on_access_type_changed(frm);

	},
    membership_type:function(frm){         
        on_membership_type_changed(frm)
    },
    duration_type:function(frm){
        on_duration_type_changed(frm)
    },
    access_type:function(frm){
        on_access_type_changed(frm)
    },
    tracking_limited:function(frm){
        on_tracking_limited_changed(frm)
    }
});


function on_membership_type_changed(frm){
    frm.set_df_property('family_pricing_section', 'hidden', 0)     
    if(frm.doc.membership_type=="Single Member"){
        frm.set_df_property('family_pricing_section', 'hidden', 1)
    }
    frm.refresh_field("family_pricing_section");
}

function on_duration_type_changed(frm){
    frm.set_df_property('membership_duration_base_on', 'hidden', 0)  
    frm.set_df_property('membership_duration', 'hidden', 0)
   
    if(frm.doc.duration_type=="Ongoing"){
        frm.set_df_property('membership_duration_base_on', 'hidden', 1)  
        frm.set_df_property('membership_duration', 'hidden', 1)
    }
    frm.refresh_field("membership_duration");
    frm.refresh_field("membership_duration_base_on");
}

function on_access_type_changed(frm){
    frm.set_df_property('duration', 'hidden', 0)  
    frm.set_df_property('per_duration', 'hidden', 0)
   
    if(frm.doc.access_type=="Unlimited"){
        frm.set_df_property('duration', 'hidden', 1)  
        frm.set_df_property('per_duration', 'hidden', 1)
    }
    frm.refresh_field("per_duration");
    frm.refresh_field("duration");
}

function on_tracking_limited_changed(frm){
    frm.set_df_property('max_access', 'hidden', 1)
    if(frm.doc.tracking_limited==1){
        frm.set_df_property('max_access', 'hidden', 0)
    }
    frm.refresh_field("max_access");
    
}