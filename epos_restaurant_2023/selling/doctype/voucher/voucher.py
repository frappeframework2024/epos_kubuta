# Copyright (c) 2024, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Voucher(Document):
	def on_submit(self):
		for payment in self.payments:
			doc = frappe.get_doc({
					'doctype':"Voucher Payment",
					'customer':self.customer,
					'payment_type':payment.payment_type,
					'posting_date':payment.posting_date,
					'working_day':self.working_day,
					'cashier_shift':self.cashier_shift,
					'payment_amount':payment.payment_amount,
					'input_amount':payment.input_amount,
					'voucher':self.name
				}).insert()
			doc.submit()

@frappe.whitelist()
def get_voucher_per_customer(customer):
	vouchers = frappe.db.get_list("Voucher",
			filters={
        'customer': customer,
		'docstatus':['in', [0,1]]
	}, order_by='creation desc',)
	if vouchers:
		voucher_list=[]
		for v in vouchers:
			voucher = frappe.get_doc('Voucher',v.name)
			voucher_list.append(voucher)
		return voucher_list
	[]
@frappe.whitelist()
def insert_voucher_multiple_row(vouchers,posauthuser):
	for v in vouchers:
		if "name" in v:
			doc = frappe.get_doc('Voucher',v["name"])
			doc.posting_date = v["posting_date"]
			doc.working_day = v["working_day"]
			doc.cashier_shift = v["cashier_shift"]
			doc.actual_amount = v["actual_amount"]
			doc.credit_amount = v["credit_amount"]
			doc.balance = v["balance"],
			doc.customer = v["customer"]
			
			doc.payments=[]
			if "payments" in v:
				main_currency = frappe.db.get_single_value("ePOS Settings", "currency")
				second_currency = frappe.db.get_value("Payment Type",payment['payment_type'],"Currency")
				exchange_rate = get_exchange_rate(main_currency,second_currency)
				frappe.throw(str(exchange_rate))
				for payment in v['payments']:
					doc.append("payments", {
						"payment_type": payment['payment_type'],
						"reference_no": payment['reference_no'] if 'reference_no' in payment else '',
						"posting_date": payment['posting_date'],
						"input_amount": payment['input_amount'],
						"payment_amount": payment['input_amount']/exchange_rate,
					})
				doc.total_paid = sum(p.payment_amount for p in doc.payments)
			doc.save()
			if len(doc.payments) > 0 and float(doc.total_paid) == float(doc.actual_amount):
				doc.submit()
		else:
			doc = frappe.get_doc({
					"doctype": "Voucher",
					"customer": v["customer"],
					"working_day": v["working_day"],
					"cashier_shift": v["cashier_shift"],
					"posting_date": v["posting_date"],
					"actual_amount": v["actual_amount"],
					"credit_amount": v["credit_amount"],
					"balance": v["credit_amount"],
					"pos_created_by" : posauthuser,
					"docstatus": v["docstatus"],
				})
			if "payments" in v:
				for payment in v['payments']:
					main_currency = frappe.db.get_single_value("ePOS Settings", "currency")
					second_currency = frappe.db.get_value("Payment Type",payment['payment_type'],"Currency")
					exchange_rate = get_exchange_rate(main_currency,second_currency)
					doc.append("payments", {
						"payment_type": payment['payment_type'],
						"reference_no": payment['reference_no'] if 'reference_no' in payment else '',
						"posting_date": payment['posting_date'],
						"input_amount": payment['input_amount'],
						"payment_amount": payment['input_amount']/exchange_rate,
						
					})
					
					
				doc.total_paid = sum(p.payment_amount for p in doc.payments) or 0
			
			doc.save()
			if len(doc.payments) > 0 and float(doc.total_paid) == float(doc.actual_amount):
				doc.submit()
		
	frappe.db.commit()

def get_exchange_rate(base_currency, second_currency):
	sql = "select exchange_rate from `tabCurrency Exchange` where from_currency='{}' and to_currency = '{}' and docstatus=1 order by posting_date desc, modified desc limit 1"
	data = frappe.db.sql(sql.format(base_currency, second_currency),as_dict=1)
	
	if len(data)> 0:
		return data[0]["exchange_rate"]
	else:
		return 1