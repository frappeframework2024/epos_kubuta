import frappe
from py_linq import Enumerable
def get_context(context):
    context.no_cache = 1
    product = frappe.get_doc("Product",frappe.form_dict.product_code)
    min_price = product.price or 0
    max_price = product.price or 0
    
    if len(product.product_price)>0:
        min_price = Enumerable(product.product_price).min(lambda x: x.price or 0)
        max_price = Enumerable(product.product_price).max(lambda x: x.price or 0)

    context.doc = product
    context.min_price = min_price
    context.max_price = max_price