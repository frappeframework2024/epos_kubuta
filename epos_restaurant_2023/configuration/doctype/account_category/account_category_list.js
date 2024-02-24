frappe.listview_settings['Account Category'] = {
    onload: function(listview) {
        
        listview.page.add_inner_button(__('Sort Order Account Category'), function() {
            let msg = frappe.msgprint(
                '<iframe src="/frontdesk/account-category-sort-order" frameBorder="0" width="100%" height="650" title="Sort Order Account Code"></iframe>',
                
                'Sort Order Account Category'
            );
            msg.$wrapper.find('.modal-dialog').css("max-width", "90%");
        });
    }
};