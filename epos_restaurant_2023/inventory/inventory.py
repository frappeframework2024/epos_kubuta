import frappe
import json

def add_to_inventory_transaction(data):
 
    doc = frappe.get_doc(data)
    # frappe.throw(str(json.dumps(data)))
    doc.insert()
    

def update_product_quantity(stock_location,product_code, quantity,cost,doc):
    if doc:
        doc.quantity =(doc.quantity or 0) + (quantity or 0)
        if cost != None:
                doc.cost = ((doc.total_cost or 0) + cost*quantity) / (doc.quantity if doc.quantity>0 else 1)  
                
        doc.total_cost = (doc.cost or 0) * (doc.quantity or 0)
        doc.save()
      
    else:
        doc = frappe.get_doc({
					'doctype': 'Stock Location Product',
					'product_code': product_code,
					'stock_location':stock_location,
					'quantity':quantity or 0,
					'cost':cost or 0,
					'total_cost':(quantity or 0) * (cost or 0)
				})
        doc.insert() 
        
def get_stock_location_product(stock_location,product_code):
    data = frappe.db.sql("select name from `tabStock Location Product` where stock_location='{}' and product_code='{}'".format(stock_location, product_code), as_dict=1)
    if data:
            return frappe.get_doc("Stock Location Product", data[0].name)
    else:
        return None

      
   

def get_uom_conversion(from_uom, to_uom):
    conversion =frappe.db.get_value('Unit of Measurement Conversion', {'from_uom': from_uom,"to_uom":to_uom}, ['conversion'], cache=True)
    
    return conversion or 1

def get_product_cost(stock_location, product_code):
    cost =frappe.db.get_value('Stock Location Product', {'stock_location':stock_location,"product_code":product_code}, ['cost'], cache=True)
    if (cost or 0) == 0:
        cost = frappe.db.get_value('Product',{'product_code':product_code}, ['cost'], cache=True)
    
    return cost or 0

def check_uom_conversion(from_uom, to_uom):
    conversion =frappe.db.get_value('Unit of Measurement Conversion', {'from_uom': from_uom,"to_uom":to_uom}, ['conversion'])
    return conversion

@frappe.whitelist(allow_guest=True)
def calculate_average_cost(product_code,stock_location,quantity,cost):
    data = frappe.db.sql("select cost,quantity,name from `tabStock Location Product` where stock_location='{}' and product_code='{}'".format(stock_location, product_code), as_dict=1)
    if data:
        current_qty = float(data[0]["quantity"])
        current_cost = float(data[0]["cost"])
        current_stock_cost = current_qty * current_cost
    else:
        current_qty = 0
        current_stock_cost = 0

    new_qty = float(quantity)
    new_cost = float(cost)
    new_stock_cost = new_cost * new_qty

    delta_cost = (current_stock_cost if current_stock_cost > 0 else 0) + new_stock_cost
    delta_qty = (current_qty if current_qty > 0 else 0) + new_qty

    avc = delta_cost / delta_qty

    return avc

@frappe.whitelist(allow_guest=True)
def get_last_inventory_transaction(product_code,stock_location,doc_name):
    data = frappe.db.sql("SELECT price FROM `tabInventory Transaction` where stock_location='{}' and product_code='{}' and transaction_number <> '{}' and docstatus = 0 order by creation desc limit 1".format(stock_location,product_code,doc_name), as_dict=1)
    if data:
       return data[0]["price"]
    else:
        return frappe.db.get_value('Product', {"name":product_code}, ['cost']) or 0
    
@frappe.whitelist(allow_guest=True)
def update_inventory_transaction_status(doc_name):
    frappe.db.sql("update `tabInventory Transaction` set docstatus = 2 where transaction_number = '{}'".format(doc_name))
    frappe.db.commit()