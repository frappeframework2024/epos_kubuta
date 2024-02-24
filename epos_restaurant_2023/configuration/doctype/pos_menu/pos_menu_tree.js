frappe.treeview_settings['POS Menu'] = {
    breadcrumb: 'POS Menu',
    title: 'POS Menu',
    fields: [
        {
            fieldtype:'Data', 
            fieldname:'pos_menu_name_en', 
            label:__('POS Menu Name EN'),
            reqd:true
        },
        {
            fieldtype:'Data', 
            fieldname:'pos_menu_name_kh', 
            label:__('POS Menu Name KH')
        },
        {
            fieldtype:'Color', 
            fieldname:'text_color', 
            label:__('Text Color')
        },
        {
            fieldtype:'Color', 
            fieldname:'background_color', 
            label:__('Background Color')
        },
        {
            fieldtype:'Link', 
            fieldname:'price_rule', 
            label:__('Price Rule'), 
            options:"Price Rule"
        },
        {
            fieldtype:'Check', 
            fieldname:'is_group', 
            label:__('Is Group')
        },
        {
            fieldtype:'Check', 
            fieldname:'shortcut_menu', 
            label:__('Shortcut Menu')
        },
    ],
    extend_toolbar: true
}
