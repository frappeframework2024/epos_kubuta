frappe.listview_settings['Account Code'] = {
    onload: function(listview) {
        
        listview.page.add_inner_button(__('Sort Order Account Code'), function() {
            let msg = frappe.msgprint(
                '<iframe src="/frontdesk/account-code-sort-order" frameBorder="0" width="100%" height="650" title="Sort Order Account Code"></iframe>',
                
                'Sort Order Account Code'
            );
            msg.$wrapper.find('.modal-dialog').css("max-width", "90%");
            
        });

        
        listview.page.add_inner_button(__('Update Folio Transaction Structure'), function() {
            
            frappe.confirm(
                'Are you sure you want to update account code structure to folio transaction?',
                function(){
                    frappe.call('edoor.api.utils.update_account_code_to_folio_transaction').then(r => {
                        frappe.show_alert('Update complete')
                    })
                    
                },
                
            )
        });

        listview.page.add_menu_item('Print Account Code', function() {
            frappe.set_route("query-report","Account Code Report")
        });

    }
};