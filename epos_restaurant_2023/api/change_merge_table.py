import json
import time
import frappe
import copy
import base64
from py_linq import Enumerable
from frappe.utils import today, add_to_date
from datetime import datetime, timedelta
from frappe import _



    
@frappe.whitelist()
def on_merge_order(old_sale, new_sale): 
    old_doc = frappe.get_doc("Sale",old_sale)
    new_doc = frappe.get_doc("Sale",new_sale)    
    change_table_sale_products = copy.deepcopy(old_doc.sale_products) 
    
    #update field in old sale of sale product 
    for c in change_table_sale_products:
        c.move_from_sale_printed  = 0
        c.move_from_sale = old_sale
        c.parent = new_sale   


    sale_products = []
    for o in new_doc.sale_products:
        sale_products.append(o)

    for a in change_table_sale_products:
        sale_products.append(a)
    
    new_doc.sale_products = sale_products  
    new_doc.save()   

    msg =""
    if old_doc.name:
        try:
            sql = "select name from `tabExtra Notification Log` where doctype_name = 'Sale' and doc_name='{}' ".format(old_sale)           
            data  =  frappe.db.sql(sql,as_dict=1)    
            if data:  
                for d in data:
                    frappe.db.sql("delete from `tabExtra Notification Log` where name = '{}'".format(d.name))                  
        except:
            pass
      
        frappe.delete_doc("Sale",old_sale)
       
        msg = "Sale document has been deleted"

    frappe.db.commit()
    new_doc = frappe.get_doc("Sale",new_sale)     
    return {"alert":msg,"data":new_doc}