frappe.listview_settings['POS Reservation'] = {
    add_fields: ['status', 'reservation_status_color','reservation_status_background_color'],
    hide_name_column: true, // hide the last column which shows the `name`
    // set this to true to apply indicator function on draft documents too
    has_indicator_for_draft: true,
    has_indicator_for_cancelled: true,

    get_indicator(doc) { 
        console.log(doc)
        return  [`<span style="font-size: 12px;background-color:${doc.reservation_status_background_color}; color:${doc.reservation_status_color}; padding: 2px 10px;border-radius: 10px;">${__(doc.status)}</span>`]; 
        
    },
}
