
import frappe
import json
from frappe.utils.response import json_handler
from datetime import datetime, timedelta
@frappe.whitelist(allow_guest=True)
def get_product_by_menu(root_menu=""):
    menus = []
    sql = """select 
                name,
                pos_menu_name_en as name_en,
                pos_menu_name_kh as name_kh,
                parent_pos_menu as parent,
                photo,
                text_color,
                background_color,
                shortcut_menu,
                price_rule,
                photo,
                'menu' as type,
                1 as type_index,
                sort_order
            from `tabPOS Menu` 
            where 
                parent_pos_menu='{}' and
                disabled = 0 
            order by sort_order, name
            """.format(root_menu)
    data = frappe.db.sql(sql,as_dict=1)
    if len(data) == 0:
        sql = """select 
                    name,
                product_category_name_en as name_en,
                product_category_name_kh as name_kh,
                parent_product_category as parent,
                photo,
                text_color,
                background_color,
                '' shortcut_menu,
                '' price_rule,
                '' photo,
                'menu' as type,
                1 as type_index,
                1 sort_order
            from `tabProduct Category` 
            where 
                coalesce(parent_product_category,'')='{}' and
                disabled = 0 
            order by sort_order, name
            """.format(root_menu)
    data = frappe.db.sql(sql,as_dict=1)

    

    for d in data:
        menus.append(d)
        
        for m in get_child_menus(d.name):
            menus.append(m)
        
        for m in get_products(d.name):
            menus.append(m)
    
    for m in get_products(root_menu):
            menus.append(m)
            
    return menus

def get_child_menus(parent_menu):
    menus = []
    menus.append({"type":"back","parent":parent_menu})
    sql = """select 
                name,
                pos_menu_name_en as name_en,
                pos_menu_name_kh as name_kh,
                parent_pos_menu as parent,
                photo,
                text_color,
                background_color,
                shortcut_menu,
                price_rule,
                'menu' as type,
                2 as type_index,
                sort_order
            from `tabPOS Menu` 
            where 
                parent_pos_menu='{}' and
                disabled = 0 
            order by sort_order, name
            """.format(parent_menu)
    data = frappe.db.sql(sql,as_dict=1)
    if len(data) == 0:
        sql = """select 
                 name,
                product_category_name_en as name_en,
                product_category_name_kh as name_kh,
                parent_product_category as parent,
                photo,
                text_color,
                background_color,
                '' shortcut_menu,
                '' price_rule,
                'menu' as type,
                2 as type_index,
                2 sort_order
            from `tabProduct Category` 
            where 
                coalesce(parent_product_category,'')='{}' and
                disabled = 0 
            order by sort_order, name
            """.format(parent_menu)
    data = frappe.db.sql(sql,as_dict=1)
    for d in data:
        
        menus.append(d)
     
        for m in get_child_menus(d.name):
            menus.append(m)
        
        for m in get_products(d.name):
            menus.append(m)
        
        
    return menus


def get_products(parent_menu):
     
    sql = """select 
                name as menu_product_name,
                product_code as name,
                product_name_en as name_en,
                product_name_kh as name_kh,
                '{0}' as parent,
                price,
                unit,
                allow_discount,
                allow_change_price,
                allow_free,
                is_open_product,
                is_inventory_product,
                is_require_employee,
                is_timer_product,
                is_open_price,
                prices,
                printers,
                modifiers,
                photo,
                'product' as type,
                3 as type_index,
                append_quantity,
                is_combo_menu,
                use_combo_group,
                combo_menu_data,
                combo_group_data,
                tax_rule,
                sort_order,
                tax_rule_data,
                revenue_group,
                sort_order
            from  `tabTemp Product Menu` 
            where 
                pos_menu='{0}' 
            order by sort_order
            """.format(parent_menu)
    data = frappe.db.sql(sql,as_dict=1)
   
    return data


@frappe.whitelist()
def get_product_variants(parent):
    data  = frappe.db.sql("select name from `tabProduct Variants` where parent='{}'".format(parent),as_dict=1)
    if data :
        return data

@frappe.whitelist()
def get_product_by_barcode(barcode,price_rule=""):
    #step 1 check barcard in tabProduct if have product return 
    #step 2 if product not exist check barcode from product price if exist retrun
    # step 3 both not exist then throw product not exist
    
    #check if barcode have in product
    data  = frappe.db.sql("select name from `tabProduct` where name='{}'".format(barcode),as_dict=1)
    if len(data) == 0:
        data  = frappe.db.sql("select name from `tabProduct` where product_code_2='{}'".format(barcode),as_dict=1)
    if len(data) == 0:
        data  = frappe.db.sql("select name from `tabProduct` where product_code_3='{}'".format(barcode),as_dict=1)
    if data:
            if data[0].name:
                p = frappe.get_doc('Product', data[0].name)
                price = p.price or 0
                if p.product_price:
                    product_price = [d for d in p.product_price if d.unit == p.unit and d.price_rule == price_rule]
                    if product_price:
                        price = product_price[0].price
                        
                return {
                    "menu_product_name": barcode,
                    "name": p.name,
                    "name_en": p.product_name_en,
                    "name_kh": p.product_name_kh,
                    "parent": p.product_category,
                    "shelf_name":p.shelf_name,
                    "price": price,
                    "unit": p.unit,
                    "allow_discount": p.allow_discount,
                    "allow_change_price": p.allow_change_price,
                    "allow_free": p.allow_free,
                    "is_open_product": p.is_open_product,
                    "is_inventory_product": p.is_inventory_product,
                    "is_timer_product":p.is_timer_product,
                    "is_open_price":p.is_open_price,
                    "prices":p.prices,
                    "printers":json.dumps(([pr.printer,pr.group_item_type] for pr in p.printers),default=json_handler),
                    "modifiers": "[]",
                    "photo": p.photo,
                    "type": "product",
                    "revenue_group":p.revenue_group,
                    "append_quantity": 1,
                    "is_require_employee":p.is_require_employee,
                    "modifiers_data": json.dumps(([pr.business_branch,pr.modifier_category,pr.prefix,pr.modifier_code,pr.price] for pr in p.product_modifiers),default=json_handler),
                    "sort_order":p.sort_order
                }
            else:
                frappe.throw("Item No Name ?")
                
    else:
        
        data  = frappe.db.sql("select name,price,unit,parent from `tabProduct Price` where barcode='{}'".format(barcode),as_dict=1)
        product = frappe.get_doc('Product', data[0].parent)
        return {
                    "menu_product_name": product.name,
                    "name": product.name,
                    "name_en": product.product_name_en,
                    "name_kh": product.product_name_kh,
                    "shelf_name":p.shelf_name,
                    "parent": product.product_category,
                    "price": data[0].price,
                    "unit": data[0].unit,
                    "allow_discount": product.allow_discount,
                    "allow_change_price": product.allow_change_price,
                    "allow_free": product.allow_free,
                    "is_open_product": product.is_open_product,
                    "is_open_price": product.is_open_price,
                    "is_timer_product": product.is_timer_product,
                    "is_inventory_product": product.is_inventory_product,
                    "prices": product.prices,
                    "printers":json.dumps(([pr.printer,pr.group_item_type] for pr in product.printers),default=json_handler),
                    "modifiers": "[]",
                    "photo": product.photo,
                    "type": "product",
                    "append_quantity": 1,
                    "is_require_employee":product.is_require_employee,
                    "revenue_group":p.revenue_group,
                    "modifiers_data": json.dumps(([pr.business_branch,pr.modifier_category,pr.prefix,pr.modifier_code,pr.price] for pr in product.product_modifiers),default=json_handler),
                    "sort_order":product.sort_order
                }
        

    frappe.throw("Product Not Found")


@frappe.whitelist()  
def get_product_price_by_price_rule(products, business_branch, price_rule=""):
    product_list = json.loads(products)
    for p in product_list:
        doc = frappe.get_doc("Product",p["product_code"])
        # check product price by price rule and branch
        price = 0
        if doc.product_price:
            price = max([d.price for d in doc.product_price if d.business_branch==business_branch and price_rule==d.price_rule]) or 0
            #check product by price rule
            if price==0:
                price = max([d.price for d in doc.product_price if price_rule==d.price_rule]) or 0
        else:
            price = doc.price
        p["price"] = price
        p["regular_price"] = price
    return json.dumps(product_list)

@frappe.whitelist()
def get_product_stock(product_code):
    products = frappe.db.sql("select product_code,stock_location,unit,quantity from `tabStock Location Product` WHERE product_code = '{0}'".format(product_code),as_dict=1)
    return products


@frappe.whitelist()
def get_product_detail_information(product_code):
    doc = frappe.get_doc("Product",product_code)
    inventory = frappe.db.sql("select stock_location,unit,quantity,reorder_level from `tabStock Location Product` where product_code='{}'".format(product_code),as_dict=1)
    
    return {"product":doc,"invenotry":inventory}
