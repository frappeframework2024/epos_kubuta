# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PriceRule(Document):
	def after_rename(self, olddn, newdn, merge=False):
		frappe.db.sql("update `tabProduct` set prices = replace(price,N'{0}',N'{1}')".format(olddn,newdn))

	def before_rename(self, olddn, newdn, merge=False):
		existed = frappe.db.exists("Price Rule",self.name)
		if existed :
			doc = frappe.get_doc("Price Rule",self.name)
			doc.previous_name = olddn
			doc.save()