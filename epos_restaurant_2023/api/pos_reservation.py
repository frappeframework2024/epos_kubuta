import json
import time
import frappe
import base64
from py_linq import Enumerable
from frappe.utils import today, add_to_date
from datetime import datetime, timedelta
import calendar
from dateutil import relativedelta
from frappe import _


@frappe.whitelist()
def get_pos_reservation_list(property,arrival_date): 
    sql = """select name from `tabPOS Reservation` 
    where case when coalesce(property,'') = '' then '{0}' else coalesce(property,'') end = '{0}'
    and arrival_date = '{1}' 
    and reservation_status in ('Confirmed')""".format(property,arrival_date)   
    get_list =  frappe.db.sql(sql,as_dict = 1)
    if get_list:
        result = []
        for g in get_list:
            doc = frappe.get_doc("POS Reservation", g.name)
            result.append(doc)

        return result
    
    else:
        return False
    