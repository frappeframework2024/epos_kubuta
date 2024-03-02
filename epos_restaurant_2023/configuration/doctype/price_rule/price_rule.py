# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PriceRule(Document):
	def after_rename(self, olddn, newdn, merge=False):
		frappe.enqueue("epos_restaurant_2023.configuration.doctype.price_rule.price_rule.update_product_prices", queue='long', self=self)

	def before_rename(self, olddn, newdn, merge=False):
		existed = frappe.db.exists("Price Rule",self.name)
		if existed :
			doc = frappe.get_doc("Price Rule",self.name)
			doc.previous_name = olddn
			doc.save()

@frappe.whitelist()
def update_product_prices(self):
	frappe.db.sql("UPDATE `tabProduct` a SET a.prices = ((SELECT CONCAT('[', GROUP_CONCAT(JSON_OBJECT('price', price, 'branch', business_branch, 'price_rule', price_rule, 'portion', b.portion, 'unit', unit, 'default_discount', default_discount)),']') FROM `tabProduct Price` b WHERE b.parent = a.name))")