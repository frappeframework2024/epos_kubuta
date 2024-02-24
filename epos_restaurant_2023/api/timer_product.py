import json
import time
import frappe
import base64
from py_linq import Enumerable
from frappe.utils import today, add_to_date
import datetime
from frappe import _
from frappe.utils.data import add_to_date,getdate
from epos_restaurant_2023.inventory.inventory import get_uom_conversion

@frappe.whitelist()
def get_timer_product_estimate_price_test():
    sale_product = {
        "name":"01f2e92b0f",
        "product_code": "T001",
        "time_in":"2024-01-09 00:03:32",
        "time_out":"2024-01-09 23:52:55",
        "parent":"SO2024-0075"
    }
    return get_timer_product_estimate_price(sale_product)

@frappe.whitelist()
def get_timer_product_breakdown_test():
    sale_product = {
        "name":"01f2e92b0f",
        "product_code": "T001",
        "time_in":"2024-01-09 00:03:32",
        "time_out":"2024-01-09 23:52:55",
        "parent":"SO2024-0075",
        "price_rule":"Normal"
    }
    return get_timer_product_breakdown(sale_product)




@frappe.whitelist(methods="POST")
def get_timer_product_estimate_price(sale_product):
    data = get_timer_product_breakdown(sale_product)
    return sum([d["amount"] for d in data])


@frappe.whitelist(methods="POST")
def get_timer_product_breakdown(sale_product):
    if "time_out" not in sale_product:
        sale_product["time_out"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not sale_product["time_out"]:
        sale_product["time_out"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    data = get_times(sale_product)
    
    product = frappe.get_doc("Product", sale_product["product_code"])
    

    #round up  time
    group_row = 0
    for d in data:
        # round up time
        round_up = ([int(x.roundup_value) for x in product.roundup_list if str(x.base_value) == str(d["total_minute"])  ]) 
        d["minute_round_up"] = d["total_minute"] if len(round_up) == 0 else max(round_up)
        # price 
        if len(product.product_price)>0:
            # return product.product_price
            prices = [x for x in product.product_price  if int(d["hour"])>=int(x.start_time) and int(d["hour"])<=int(x.end_time) and x.price_rule == sale_product["price_rule"] ]
            

            if len(prices)>0:
                d["price"]  = prices[0].price
                d["unit"] = prices[0].unit
                d["portion"] = prices[0].portion
                d["uom_conversion"] = get_uom_conversion(product.unit,prices[0].unit)
                
            else:
                d["unit"] = product.unit
                d["price"] = product.price or 0
                d["uom_conversion"] = 1
                d["portion"] = ""
            
        else:
            d["unit"] = product.unit
            d["price"] = product.price or 0
            d["uom_conversion"] = 1
            d["portion"] = ""

        d["base_price"] = d["uom_conversion"] * d["price"]
        d["amount"] = d["minute_round_up"] * d["uom_conversion"] * d["price"]

        
        if data.index(d)>0:
            if getdate(d["time_in"]) != getdate(data[data.index(d)-1]["time_in"]) or d["price"]  != data[data.index(d)-1]["price"]:
                group_row = group_row + 1

        d["group_row"] = group_row 

    group_rows = set([d["group_row"] for d in data])
    
    breakdown_data = []
    
    for n in group_rows:
        records = [d for d in data if d["group_row"] == n]

        record =  ({
            "time_in":min([d["time_in"] for d  in  records]),
            "time_out_price": max([d["time_out"] for d  in  records]),
            "time_out":   max([d["time_out"] for d  in  data]) if n == 0 else None,
            "price":  max([d["price"] for d  in  records]),
            "base_price":  max([d["base_price"] for d  in  records]),
            "amount":  sum([d["amount"] for d  in  records]),
            "total_minute": sum([d["minute_round_up"] for d  in  records]),
            "reference_sale_product": sale_product["name"] if n > 0 else None,
            "portion": "" if len(records)==0 else records[0]["portion"]
        })
        record["duration"]  ="{}h {}mn".format(record["total_minute"] // 60,record["total_minute"] % 60)
        breakdown_data.append(record)

    return breakdown_data


@frappe.whitelist(methods="POST")
def stop_timer(sale_product):
    time_in =  datetime.datetime.strptime(str(sale_product["time_in"]), "%Y-%m-%d %H:%M:%S")
    time_out =  datetime.datetime.strptime(str(sale_product["time_out"]), "%Y-%m-%d %H:%M:%S")

    if time_out<=time_in:
        frappe.throw("Time out must be greater than time in")
        

    if "parent" not in sale_product:
         frappe.throw(_("Please submit order first"))
    
    if "name" not in sale_product :
        frappe.throw(_("Please submit order first"))
    
    breawkdown_data = get_timer_product_breakdown(sale_product)
    
    sale_doc = frappe.get_doc("Sale", sale_product["parent"])

    data  =  [d for d in  sale_doc.sale_products if d.name == sale_product["name"]]
    if len(data) == 0:
         frappe.throw(_("Sale product record not found"))
    base_record = data[0]
    base_record.time_in = breawkdown_data[0]["time_in"]
    base_record.time_out_price = breawkdown_data[0]["time_out_price"]
    base_record.price = breawkdown_data[0]["base_price"]
    base_record.quantity = breawkdown_data[0]["total_minute"]
    base_record.duration = breawkdown_data[0]["duration"]
    base_record.time_out = breawkdown_data[0]["time_out"]
    base_record.portion = breawkdown_data[0]["portion"]
    

    for d in breawkdown_data:
        if breawkdown_data.index(d)> 0:
            # Create a new child document
            child_doc = frappe.new_doc("Sale Product")
            child_doc.product_code= sale_product['product_code']
            child_doc.quantity = d["total_minute"]
            child_doc.time_in = d["time_in"]
            child_doc.time_out_price = d["time_out_price"]
            child_doc.price= d["base_price"]
            child_doc.reference_sale_product = sale_product["name"]
            child_doc.order_by = sale_product["order_by"]
            child_doc.order_time = sale_product["order_time"]
            child_doc.is_require_employee = 0
            child_doc.is_timer_product = 1
            child_doc.duration = d["duration"]
            child_doc.portion = d["portion"]
            child_doc.discount_type = sale_product["discount_type"]
            child_doc.discount= sale_product["discount"]
            sale_doc.append("sale_products", child_doc)


    sale_doc.save()
    return sale_doc



@frappe.whitelist(methods="POST")
def continue_timer(sale_product):
    if "parent" not in sale_product:
         frappe.throw(_("Please submit order first"))
    
    if "name" not in sale_product :
        frappe.throw(_("Please submit order first"))
    
    sale_doc = frappe.get_doc("Sale", sale_product["parent"])
    data  =  [d for d in  sale_doc.sale_products if d.name == sale_product["name"]]
    if len(data) == 0:
         frappe.throw(_("Sale product record not found"))
    base_record = data[0]
    base_record.time_out_price = None
    base_record.price = 0
    base_record.quantity = 0
    base_record.duration = None
    base_record.time_out = None
    base_record.portion = None

    sale_doc.save()
    
    frappe.db.sql("delete from `tabSale Product` where reference_sale_product='{}' and parent='{}'".format(sale_product["name"],sale_product["parent"]))
    
    frappe.db.commit()
    return  frappe.get_doc("Sale", sale_product["parent"])

    
    

def get_times(sale_product):
    times = []
    time_in = datetime.datetime.strptime(sale_product["time_in"], "%Y-%m-%d %H:%M:%S")
    time_out = datetime.datetime.strptime(sale_product["time_out"], "%Y-%m-%d %H:%M:%S")

    while time_in<= time_out:
        times.append(
            { 
            "time_in": time_in.replace(minute=00, second=00),
            "time_out": add_to_date(time_in,hours=1).replace(minute=0, second=0)
        }
        )
        time_in = add_to_date(time_in, hours = 1)
       
  
    if len(times)> 0:
        times[0]["time_in"] = datetime.datetime.strptime(sale_product["time_in"], "%Y-%m-%d %H:%M:%S").replace(second=0)
        times[len(times)-1]["time_out"] = datetime.datetime.strptime(sale_product["time_out"], "%Y-%m-%d %H:%M:%S").replace(second=0)
    
    for d in times:
        time_in = datetime.datetime.strptime(str(d["time_in"]), "%Y-%m-%d %H:%M:%S")
        time_out = datetime.datetime.strptime(str(d["time_out"]), "%Y-%m-%d %H:%M:%S")
       
        d["total_minute"] =  int((time_out - time_in).total_seconds() / 60)
        d["hour"] = time_in.hour


    return times

 