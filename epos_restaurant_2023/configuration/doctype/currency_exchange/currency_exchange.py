# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CurrencyExchange(Document):
	def validate(self):
		if self.exchange_rate_input <= 0 or self.change_exchange_rate_input <= 0:
			frappe.throw("Input values cannot less than or equal zero.")
		
		if  frappe.db.get_default("currency") == self.from_currency:
			self.exchange_rate = self.exchange_rate_input
			self.change_exchange_rate = self.change_exchange_rate_input
		else:
			if frappe.db.get_default("exchange_rate_main_currency") == self.from_currency and    frappe.db.get_default("currency")  != frappe.db.get_default("exchange_rate_main_currency"):
				self.exchange_rate = 1/ self.exchange_rate_input
				self.change_exchange_rate = 1/self.change_exchange_rate_input
		
		if self.from_currency == self.to_currency:
			self.exchange_rate_input = 1
			self.exchange_rate = 1

			## change exchange rate 
			self.change_exchange_rate_input = 1
			self.change_exchange_rate = 1

	def on_submit(self):
		currency = self.to_currency
		if frappe.db.get_default("exchange_rate_main_currency") == self.from_currency and    frappe.db.get_default("currency")  != frappe.db.get_default("exchange_rate_main_currency"):
			currency = self.from_currency

		# update payment type  exchange rate
		sql_payment_type = "update `tabPayment Type` set exchange_rate = {}, change_exchange_rate = {} where currency='{}'".format(self.exchange_rate,self.change_exchange_rate,currency)
		frappe.db.sql(sql_payment_type)		

		#update to pos config payment type exchange rate
		sql_config_payment_type = "update `tabPOS Config Payment Type` set exchange_rate = {},change_exchange_rate = {} where currency='{}'".format(self.exchange_rate,self.change_exchange_rate,currency)
		frappe.db.sql(sql_config_payment_type)


