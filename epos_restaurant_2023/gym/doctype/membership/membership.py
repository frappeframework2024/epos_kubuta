# Copyright (c) 2023, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
# from datetime import timedelta, date
from frappe.model.document import Document


class Membership(Document):
	def validate(self):
		if self.membership_type =="Family Shared":
			if self.count_members <=0:
				frappe.throw("Your counter member not allow value less than zero(0).")
			
			if not self.membership_family_table and self.count_members > 1:
				frappe.throw("Please add members to list for Family Shared")

			elif len(self.membership_family_table) >= self.count_members:
				frappe.throw("List of members cannot allow more than {}".format(self.count_members - 1))
			elif len(self.membership_family_table) < (self.count_members - 1):
				frappe.throw("Member list not enough, please add more")
		


		if self.discount_type=="Percent":
			self.total_discount = ((self.price or 0) * (self.discount or 0)/100)
			self.grand_total = (self.price or 0) - self.total_discount
		else:
			self.total_discount =  (self.discount or 0)
			self.grand_total = (self.price or 0) - self.total_discount
		
		#update date balance
		self.balance = self.grand_total - (self.total_paid or 0)
		

	def on_submit(self):
		update_membership(self)
	
	def on_cancel(self):
		update_membership(self)


def update_membership(self):
	data = frappe.db.sql("select ifnull(sum(balance),0)  as total_balance from `tabMembership` where docstatus=1 and customer='{}' and balance>0".format(self.customer))
	frappe.db.set_value('Customer', self.customer,  {
		'balance': data[0][0]
	})

