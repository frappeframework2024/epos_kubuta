from epos_restaurant_2023.api.api import get_system_settings
import frappe

@frappe.whitelist(allow_guest=True)
def on_check_url():  
    return True

@frappe.whitelist(allow_guest=True) 
def on_get_pos_configure(pos_profile="", device_name=''):  
    return get_system_settings(pos_profile,device_name) 