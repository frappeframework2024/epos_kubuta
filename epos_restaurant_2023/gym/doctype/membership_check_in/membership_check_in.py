# Copyright (c) 2023, Tes Pheakdey and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document


class MembershipCheckIn(Document): 
	def on_submit(self): 
		for m in self.membership_check_in_item:			
			sql = """select count(`name`) as total_check_in from `tabMembership Check In Items` 
					where membership = '{}' 
					and docstatus = 1 """.format( m.membership)
			
		 
			exec = frappe.db.sql(sql, as_dict=1)
			# frappe.throw(str(exec))
			# frappe.throw(str(sql))
			if exec:
				count = (exec[0].total_check_in or 0)
				update = "update `tabMembership Check In Items` set check_in_number = {} where name ='{}'".format(count,m.name) 
				frappe.db.sql(update)



	