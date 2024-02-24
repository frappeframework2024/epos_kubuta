import frappe
def get_context(context):
    
    data = frappe.db.sql("""
                    select 
                        name,
                        product_name_en,
                        product_name_kh,
                        photo
                    from `tabProduct`
    """, as_dict=1)

    
    context.data = data