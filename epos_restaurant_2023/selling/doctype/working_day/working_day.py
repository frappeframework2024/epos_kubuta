# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import NamingSeries
from frappe.utils.print_format import download_pdf

class WorkingDay(Document):
    
	def validate(self):

	 

		if self.is_new():
			if frappe.db.exists('Working Day', {'pos_profile': self.pos_profile, 'is_closed': 0}):
				frappe.throw("Workingday in this pos profile {} is already opened".format(self.pos_profile))
		
	


		#if close shift check current bill open 
		if self.is_closed==1:
			# validate cashier shift open 
			pending_cashier_shift = frappe.db.sql("select name from `tabCashier Shift` where is_closed  = 0 and working_day = '{}'".format(self.name), as_dict=1)
			if pending_cashier_shift:
				frappe.throw("Please close cashier shift first.")
			#Validate Allow Closed Working Day when when has bill
			pos_config = frappe.db.get_value('POS Profile', self.pos_profile, 'pos_config')
			allow_closed_working_day_when_has_pending_order = frappe.db.get_value('POS Config', pos_config, 'allow_closed_working_day_when_has_pending_order')
			if allow_closed_working_day_when_has_pending_order == 0:
				pending_orders = frappe.db.sql("select name from `tabSale` where docstatus = 0 and working_day = '{}'".format(self.name), as_dict=1)
				if pending_orders:
					frappe.throw("Please close all pending order before closing working day.")

			#check reset waiting number
			pos_profile = frappe.get_doc("POS Profile", self.pos_profile)
			if pos_profile.reset_waiting_number_after=="Close Working Day":
				prefix = pos_profile.waiting_number_prefix.replace('.','').replace("#",'')
				naming_series = NamingSeries(prefix)
				naming_series.update_counter(0)
			# self.send_mail_closed_day()


	# def send_mail_closed_day(self):
	# 	reports_name = ['Working Day Sale Transaction','Working Day Sale Summary V2','Working Day Sale Product Summary']
	# 	print_formats=[]
	# 	for name in reports_name:
	# 		print_formats.append({'fname':f"{name}_{self.posting_date}.pdf",'fcontent':frappe.get_print(doctype=self.doctype, name=self.name, print_format=name)})
	# 	download_pdf("Working Day", name, format=None, doc=None, no_letterhead=0)

	# 	frappe.sendmail(
	# 		recipients='sengho.estc@gmail.com',
	# 		sender='sengho.kimsea@estccomputer.com',
	# 		subject=f'Closed Working Day In {self.posting_date}',
	# 		content='Working Day Was Close',
	# 		header=[f'Closed Working Day In {self.posting_date}', "green"],
	# 		attachments=print_formats
	# 	)