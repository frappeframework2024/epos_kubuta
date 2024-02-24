// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Membership", {
	refresh(frm) {
           
	},
    onload(frm){
        if((frm.doc.end_date||"")!=""){           
            if((frm.doc.regular_end_date||"")==""){
                frm.set_df_property('regular_end_date', 'hidden', 0);
                frm.doc.regular_end_date =frm.doc.end_date;
                frm.set_df_property('regular_end_date', 'hidden', 1);
            }            
        }
console.log(frm.doc)
        on_membership_value_changed(frm)   
    },
    is_delay_access:function(frm){
        on_is_delay_access_value_changed(frm,true)
    },
    membership:function(frm){
        on_membership_value_changed(frm,true )
    },
    duration_type:function(frm){        
        on_duration_type_value_changed(frm,true)
    },
    membership_type:function(frm){
        on_membership_type_value_changed(frm,true)
    },
    start_date:function(frm){
        on_start_date_changed(frm,true)
    },
    access_type:function(frm){
        on_access_type_value_changed(frm,true)
    },
    price:function(frm){
        on_price_value_changed(frm,true)
    },
    discount_type:function(frm){
        on_price_value_changed(frm,true)
    },
    discount:function(frm){
        on_price_value_changed(frm,true)
    },
    count_members:function(frm){
        on_count_members_value_changed(frm,true)
    },
    tracking_limited:function(frm){
        on_tracking_limited_changed(frm,true);       
    },
    delay_access:function(frm){
        on_delay_access_value_changed(frm,true);
    }
});

function on_membership_value_changed(frm,changed=false){ 
    on_duration_type_value_changed(frm,changed);
    on_membership_type_value_changed(frm,changed);
    on_access_type_value_changed(frm,changed);
    on_tracking_limited_changed(frm,changed);
    on_is_delay_access_value_changed(frm,changed);

    if(frm.doc.membership != "" && frm.doc.membership!=undefined){
        if(changed){
            frappe.db.get_value("Membership Options",frm.doc.membership,["*"]).then((r)=>{
                frm.doc.price = r.message.cost;
                on_update_grand_total(frm,changed);
                frm.refresh_field("price");   
            });
        }else{
            on_update_grand_total(frm,changed);
        }        
    }

    frm.set_df_property('duration_type', 'hidden', 0);
    frm.set_df_property('access_to_training_section', 'hidden', 0);
    if(frm.doc.membership=="" || frm.doc.membership == undefined){
        frm.set_df_property('duration_type', 'hidden', 1); 
        frm.set_df_property('access_to_training_section', 'hidden', 1); 
        
    } 
    if(changed){
        frm.refresh_field("duration_type");   
        frm.refresh_field("access_to_training_section");  
    } 
}

function on_duration_type_value_changed(frm,changed=false){ 
    frm.set_df_property('start_date', 'hidden', 0);
    frm.set_df_property('end_date', 'hidden', 0);
    if(frm.doc.duration_type =="Ongoing" || frm.doc.membership=="" || frm.doc.membership == undefined){
        frm.set_df_property('start_date', 'hidden', 1);
        frm.set_df_property('end_date', 'hidden',1);
    }else{
        if(frm.doc.duration_type=="Limited Duration"){
            on_start_date_changed(frm,changed)            
        }
    }
    if(changed){
        frm.refresh_field("start_date");
        frm.refresh_field("end_date");  
    }  
}

function on_start_date_changed(frm,changed=false){
    if(changed){
        frm.set_df_property('end_date', 'read_only', 0);
        const _date = new Date(frm.doc.start_date);  
        const _duration =   frm.doc.membership_duration;   
        let _end_date = _date;
        switch(frm.doc.duration_base_on){
            case 'Day(s)':
                _end_date = new Date(_date.setDate(_date.getDate() + _duration));   
                break
            case 'Week(s)':
                _end_date = new Date(_date.setDate(_date.getDate() + (_duration * 7) - 1));   
                break;
            case 'Month(s)':
                const new_month = new Date(_date.setMonth(_date.getMonth() +_duration)); 
                _end_date =  new Date(new_month.setDate(new_month.getDate() -1)); 
                break;
            case 'Year(s)':
                const new_year = new Date(_date.setFullYear(_date.getFullYear() +_duration)); 
                _end_date =  new Date(new_year.setDate(new_year.getDate() -1)); 
                break;
            default:
                _end_date  = frm.doc.start_date;
                break;
        }  

        frm.set_df_property('regular_end_date', 'hidden', 0);
        frm.doc.regular_end_date = new Date(_end_date);  
        frm.refresh_field("regular_end_date"); 
        frm.set_df_property('regular_end_date', 'hidden', 1);
        

        // check delay access
        if(frm.doc.is_delay_access==1){
            const _end = new Date(_end_date)
            const _delay_access_value =   frm.doc.delay_access; 
            switch(frm.doc.delay_access_base_on){
                case 'Day(s)':
                    _end_date = new Date(_end.setDate(_end.getDate() + _delay_access_value));   
                    break;
                case 'Month(s)':
                    const _new_month = new Date(_end.setMonth(_end.getMonth() +_delay_access_value)); 
                    _end_date =  new Date(_new_month.setDate(_new_month.getDate())); 
                    break;
                default:
                    _end_date = _end_date;
                    break;
            }
        }

        frm.doc.end_date = _end_date;  
        frm.refresh_field("end_date"); 
       
    } 
    frm.set_df_property('end_date', 'read_only', 1);
    
}

function on_membership_type_value_changed(frm,changed=false){
    frm.set_df_property('family_shared_section', 'hidden', 0);
    if(frm.doc.membership_type=="" || frm.doc.membership_type=="Single Member" || frm.doc.membership_type==undefined){
        frm.set_df_property('family_shared_section', 'hidden', 1); 
    }
    if(changed){
        frm.doc.count_members = 0;
        frm.refresh_field("count_members");   
        frm.refresh_field("family_shared_section");   
    }
}

function on_access_type_value_changed(frm,changed=false){
    frm.set_df_property('access_type', 'read_only', 0);   
    frm.set_df_property('per_duration', 'read_only', 0);   
    frm.set_df_property('duration', 'read_only', 0);  

    
    frm.set_df_property('duration', 'hidden', 0);
    frm.set_df_property('per_duration', 'hidden', 0);
    if(frm.doc.access_type=="" || frm.doc.access_type==undefined || frm.doc.access_type=="Unlimited"){
        frm.set_df_property('duration', 'hidden', 1); 
        frm.set_df_property('per_duration', 'hidden', 1); 
    } 
    

    //read only properties
    frm.set_df_property('access_type', 'read_only', 1);   
    frm.set_df_property('per_duration', 'read_only', 1);   
    frm.set_df_property('duration', 'read_only', 1);   
    if(changed){
        frm.refresh_field("duration");   
        frm.refresh_field("per_duration");   
    }
}

function on_price_value_changed(frm,changed=false){
    on_update_grand_total(frm,changed)
}


function on_update_grand_total(frm, changed=false){
    frm.set_df_property('grand_total', 'read_only', 0);   
    if(frm.doc.discount_type=="Percent"){
        frm.doc.grand_total = (frm.doc.price||0) - ((frm.doc.price||0) * (frm.doc.discount||0)/100)
    }else{
        frm.doc.grand_total = ((frm.doc.price||0) - (frm.doc.discount||0))
    }
 
    frm.doc.balance =  (frm.doc.grand_total||0) - (frm.doc.total_paid||0); 
    frm.set_df_property('grand_total', 'read_only', 1);    

    if(changed){
        frm.refresh_field("balance");  
        frm.refresh_field("grand_total");  
    }
}

function on_count_members_value_changed(frm,changed=false){
    if(changed){
        frappe.db.get_doc("Membership Options",frm.doc.membership).then((r)=>{
            if((frm.doc.count_members||1) > 1){ 
              var number_of_member =  r.family_members_table.filter((x)=>x.number_of_member == frm.doc.count_members);
              if(number_of_member.length>0){
                frm.doc.price = number_of_member[0].cost;
                on_update_grand_total(frm,changed);
                frm.refresh_field("price");   
              }
            }else{
                frm.doc.price = (r.cost||0)
                on_update_grand_total(frm,changed);
                frm.refresh_field("price");   
            }
       })
        
    }
}

function on_tracking_limited_changed(frm,changed){
    frm.set_df_property('max_access', 'hidden', 1);
    if(frm.doc.tracking_limited==1){
        frm.set_df_property('max_access', 'hidden', 0);

    }
    frm.refresh_field("max_access");
}


function on_is_delay_access_value_changed(frm,changed){
    if(frm.doc.__islocal==1){
        frm.set_df_property('is_delay_access', 'hidden', 1);
        frm.set_df_property('delay_access_base_on', 'hidden', 1);
        frm.set_df_property('delay_access', 'hidden', 1);
    }else{
        if(frm.doc.is_delay_access==0){
            frm.doc.end_date = frm.doc.regular_end_date;
            frm.refresh_field("end_date"); 
            frm.set_df_property('delay_access_base_on', 'hidden', 1);
            frm.set_df_property('delay_access', 'hidden', 1);
        }else{
            
            frm.set_df_property('delay_access_base_on', 'hidden', 0);
            frm.set_df_property('delay_access', 'hidden', 0);
            on_delay_access_value_changed(frm,changed)
        } 
    }
}

function on_delay_access_value_changed(frm, changed){
    frm.set_df_property('end_date', 'read_only', 0);
    const _date = new Date(frm.doc.regular_end_date);   
    const _duration =   frm.doc.delay_access;   
    let _end_date = _date;
    switch(frm.doc.delay_access_base_on){
        case 'Day(s)':
            _end_date = new Date(_date.setDate(_date.getDate() + _duration));   
            break;
        case 'Month(s)':
            const _new_month = new Date(_date.setMonth(_date.getMonth() +_duration)); 
            _end_date =  new Date(_new_month.setDate(_new_month.getDate())); 
            break;
        default:
            break;
    }      
    frm.doc.end_date = new Date(_end_date) ;   
    frm.refresh_field("end_date"); 

    frm.set_df_property('end_date', 'read_only', 1);
}