# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class SalePayment(Document):
	def validate(self):
		#check if reservation deleted
		if self.pos_reservation:
			reservation = frappe.get_doc("POS Reservation", self.pos_reservation)			
			if reservation.reservation_status != "Confirmed" and not self.sale:
				frappe.throw("Payment not allow with this current reservation status. ({})".format(reservation.reservation_status))

			# frappe.throw("The pos reservation {} was void.".format(self.pos_reservation))
		else:
			if not self.sale:
				frappe.throw("Mandatory fields required in Sale Payment (Sale*)")

		# check if payment type is on-account
		if self.payment_type_group == "On Account":
			frappe.throw("Payment {} {}".format(self.payment_type,_("is not allow to process pay")))

		if (self.exchange_rate or 0) ==0 or self.currency == frappe.db.get_default("currency"):
			self.exchange_rate = 1
			self.change_exchange_rate = 1
		
		currency_precision = frappe.db.get_single_value('System Settings', 'currency_precision')
		if self.transaction_type =="Changed":
			self.payment_amount = self.input_amount / self.change_exchange_rate 
		else:
			self.payment_amount = self.input_amount / self.exchange_rate 
		
		self.payment_amount = round(self.payment_amount,int(currency_precision))
		
   		
		if (self.payment_amount or 0) ==0:
			frappe.throw(_("Please enter payment amount"))
   
		if self.sale:
			#validate expense if is a submitted expense
			sale_status = frappe.db.get_value("Sale",self.sale,"docstatus")
			
			if not sale_status==1:
				frappe.throw(_("This sale is not submitted yet"))

			#check paid amount cannot over balance
			if self.check_valid_payment_amount:
				if self.payment_amount > self.balance:
					frappe.throw("Payment amount cannot greater than sale balance")
		

	def on_submit(self):
		update_sale(self)
	
	def on_cancel(self):
		update_sale(self)

	def before_update_after_submit(self):
		if not self.sale:
			self.sale_date = None
			self.customer = None
			self.customer_name = None
			self.customer_group = None
			self.pos_profile = None
			self.outlet = None
			self.business_branch = None
			self.working_day = None
			self.cashier_shift = None
			self.sale_amount = 0
			self.total_paid = 0
			self.balance = 0

		update_sale(self)


def update_sale(self):
	currency_precision = frappe.db.get_single_value('System Settings', 'currency_precision')
	if currency_precision=='':
			currency_precision = "2"

	_deposit = 0
	#update reservation deposit		
	if self.pos_reservation:
		if self.is_reservation_deposit:
			_sql1 = """select 
				ifnull(sum(payment_amount),0)  as total_deposit 
			from `tabSale Payment` 
			where pos_reservation='{}' 
				and is_reservation_deposit=1 
				and docstatus=1 
				and payment_amount > 0""".format(self.pos_reservation)
			_data = frappe.db.sql(_sql1)
			if _data:
				_deposit = round(_data[0][0],int(currency_precision))
				frappe.db.set_value("POS Reservation",self.pos_reservation,{
					"total_deposit":_deposit
				})

	# update sale balance and paid
	if self.sale:
		data = frappe.db.sql("select  ifnull(sum(payment_amount),0)  as total_paid from `tabSale Payment` where docstatus=1 and sale='{}' and payment_amount>0".format(self.sale))
		sale_amount = frappe.db.get_value('Sale', self.sale, 'grand_total')
		if data and sale_amount:
			balance =round(sale_amount,int(currency_precision))-round(data[0][0], int(currency_precision))  

			if balance<0:
				balance = 0
			frappe.db.set_value('Sale', self.sale,  {
				'total_paid': round(data[0][0],int(currency_precision)),
				'balance': balance
			})

		# update customer balance 
	

