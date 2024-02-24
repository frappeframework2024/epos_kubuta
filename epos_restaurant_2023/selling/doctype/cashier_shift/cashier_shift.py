# Copyright (c) 2022, Tes Pheakdey and contributors
# For license information, please see license.txt
import json
from py_linq import Enumerable
import frappe
from frappe.model.document import Document
from frappe.model.naming import NamingSeries
class CashierShift(Document):
	def validate(self):
		# #if close shift check current bill open 
		# if self.is_closed==1:
		# 	pending_orders = frappe.db.sql("select name from `tabSale` where docstatus = 0 and cashier_shift = '{}'".format(self.name), as_dict=1)
		# 	if pending_orders:
		# 		frappe.throw("Please close all pending order before close cashier shift.")

		if self.is_new() == 1:
			if 'edoor' in frappe.get_installed_apps():
				if self.is_edoor_shift==0:
					current_edoor_shift = frappe.get_list("Cashier Shift",
											filters={
												"business_branch":self.business_branch, 
												"is_closed":0,
												"shift_name":self.shift_name,
												"is_edoor_shift":1,
												"name":['!=',self.name]
											},fields=['name', 'shift_type'])
					if not current_edoor_shift:
						frappe.throw("Invalid shift name please try again")


			
			data = frappe.get_list("Cashier Shift",filters={"pos_profile":self.pos_profile,"business_branch":self.business_branch, "is_closed":0})
			if data:
				frappe.throw("Cashier shift is already opened")

				
				

		for c in self.cash_float:
			exchange_rate = frappe.get_value("Payment Type", c.payment_method,"exchange_rate")
			exchange_rate = exchange_rate or 1
			c.exchange_rate = exchange_rate
			
			c.opening_amount = float(c.input_amount) / exchange_rate
			c.close_amount = float(c.input_close_amount) / exchange_rate
			c.system_close_amount = float(c.input_system_close_amount) / exchange_rate

			c.different_amount = (c.close_amount or 0) - (c.system_close_amount or 0)

		for c in self.cash_count:
			c.total_base_currency_amount = (c.total_amount or 0) / (c.exchange_rate or 1)
			
		self.total_opening_amount = Enumerable(self.cash_float).sum(lambda x: x.opening_amount)
		self.total_system_close_amount = Enumerable(self.cash_float).sum(lambda x: x.system_close_amount)
		self.total_close_amount = Enumerable(self.cash_float).sum(lambda x: x.close_amount)
		self.total_different_amount = self.total_close_amount -  self.total_system_close_amount

		# check if close shift then check 
		if self.is_closed==1:
			if self.is_run_night_audit==1:
				#validte if still have epos open
				if frappe.db.exists("Cashier Shift",{"is_closed":0, "is_edoor_shift":0}):
					frappe.throw("Please close pos cashier first")
				#validate if staill have sale order pending
				if frappe.db.exists("Sale",{"docstatus":0}):
					frappe.throw("Please close all pending order in POS first")


			if not self.closed_by:
				self.closed_by = frappe.session.user

			self.closed_date = frappe.utils.now()
			pos_profile = frappe.get_doc("POS Profile", self.pos_profile)
			if pos_profile.reset_waiting_number_after=="Close Cashier Shift":
				prefix = pos_profile.waiting_number_prefix.replace('.','').replace("#",'')
				naming_series = NamingSeries(prefix)
				naming_series.update_counter(0)
			

			# check if have edoor app for generate FB revenue to Folio Transaction group by acc.code
			if 'edoor' in frappe.get_installed_apps() and self.is_edoor_shift == 0:
				#validate account code for post to folio transaction
				validate_pos_account_code_config(self)
				
				
				       
			
			is_upload_sale_data_to_google_sheet = frappe.db.get_value("Business Branch",self.business_branch,["upload_sale_data_to_google_sheet"])
			if is_upload_sale_data_to_google_sheet == 1:
				frappe.enqueue("epos_restaurant_2023.api.api.upload_all_sale_data_to_google_sheet",start_date=self.posting_date,end_date = self.posting_date,business_branch=self.business_branch,cashier_shift=self.name)

	def after_insert(self):	
		query ="update `tabSale` set working_day='{}', cashier_shift='{}', shift_name='{}' "
		query = query + " where docstatus = 0 and pos_profile = '{}'"

		query = query.format(self.working_day, self.name,self.shift_name, self.pos_profile)

		frappe.db.sql(query)

	def on_update(self):
		query ="update `tabSale` set  shift_name='{}' where cashier_shift='{}'".format(self.shift_name,self.name)
		frappe.db.sql(query)
		if 'edoor' in frappe.get_installed_apps():
			old_doc = self.get_doc_before_save()
			if old_doc:
				if old_doc.is_closed ==0 and self.is_closed ==1:
					current_sort = frappe.db.get_value("Shift Type",self.shift_name, "sort")
					 
					if self.is_edoor_shift==1 and  self.is_run_night_audit==0:
						if current_sort != 3:
							"""Create New Cashier Shift When Close Shift eDoor"""
							new_shift_data = {
								"doctype":"Cashier Shift",
								"bussiness_branch": self.business_branch,
								"outlet":self.outlet,
								"pos_profile":self.pos_profile,
								"working_day":self.working_day,
								"is_edoor_shift":self.is_edoor_shift,
								"cash_float":[]
							}
							
	
							if current_sort == 1:
								next_shift_name = frappe.db.get_value("Shift Type",{'sort': 2} , "name")
								new_shift_data["shift_name"] = next_shift_name
							elif current_sort == 2:
								next_shift_name = frappe.db.get_value("Shift Type",{'sort': 3} , "name")
								new_shift_data["shift_name"] = next_shift_name
							
							pos_config = frappe.db.get_value("POS Profile", self.pos_profile, "pos_config")
							pos_config = frappe.get_doc("POS Config", pos_config)

							for  c in pos_config.payment_type:
								if c.allow_cash_float:
									new_shift_data["cash_float"].append({
										"payment_method":c.payment_type,
										"currency":c.currency,
										"input_amount":0
									})
							
							frappe.get_doc(new_shift_data).insert()

					else:
						frappe.enqueue("epos_restaurant_2023.selling.doctype.cashier_shift.cashier_shift.submit_pos_data_to_folio_transaction", queue='short', self=self)



# get sale product revenue sum group by
def get_sale_product_revenue(sale_products):
	sale_product_revenue ={
		"revenue_group":sum_revenue_by_field(sale_products,field_account="account_code",field_amount="revenue_amount"),
		"discount":sum_revenue_by_field(sale_products,field_account="discount_account",field_amount="discount_amount"),
		"tax_1":sum_revenue_by_field(sale_products,field_account="tax_1_account",field_amount="tax_1_amount"),
		"tax_2":sum_revenue_by_field(sale_products,field_account="tax_2_account",field_amount="tax_2_amount"),
		"tax_3":sum_revenue_by_field(sale_products,field_account="tax_3_account",field_amount="tax_3_amount")
	}

	return sale_product_revenue
 
# sale prduct sum group by with field
def sum_revenue_by_field(sale_products,field_amount,field_account):
	result = []
	groups = {}
	for row in sale_products:
		group = {
				"cashier_shift":row["cashier_shift"],
				"outlet": row["outlet"],
				"shift_name":row["shift_name"],
				"revenue_group":row["revenue_group"],
				"revenue_code":row["revenue_code"],
				field_account:row[field_account]
			}
		
		_field_amount = row[field_amount]
		g = json.dumps(group)	  
		if g not in groups:
			groups[g] = {field_amount: []} 

		groups[g][field_amount].append(_field_amount)


	for group, total in groups.items():	 
		total_amount = sum(total[field_amount])
		g = json.loads(group)	
		
		_result = {}
		_result.update({
			"revenue_code":g["revenue_code"],
			"account":(g[field_account] or ""),
			"amount":(total_amount or 0)
			})	

		result.append(_result)	

	return result


def get_sale_payment(sale_payments):

	result = []
	groups = {}
	for row in sale_payments:
		group = {				
				"payment_type_group": row["payment_type_group"],
				"account_code":row["account_code"]
			}
		
		payment_amount = row['payment_amount']
		fee_amount = row['fee_amount']
		g = json.dumps(group)	  
		if g not in groups:
			groups[g] = {'payment_amount': [],'fee_amount':[]} 

		groups[g]['payment_amount'].append(payment_amount)
		groups[g]['fee_amount'].append(fee_amount)


	for group, total in groups.items():	 
		total_amount = sum(total['payment_amount'])
		total_fee = sum(total['fee_amount'])
		g = json.loads(group)	
		
		_result = {}
		_result.update({
			"payment_type_group":(g['payment_type_group'] or ""),
			"account":(g['account_code'] or ""),
			"amount":(total_amount or 0),
			"fee_amount":(total_fee or 0),
			})	
		result.append(_result)	
	
	return result

def validate_pos_account_code_config(self):
	account_code_config = frappe.db.get_list("POS Account Code Config", filters={"outlet":self.outlet, "shift_name":self.shift_name})
	config = None
	if account_code_config:
		config =  frappe.get_doc("POS Account Code Config",account_code_config[0].name)
	if not config:
		frappe.throw("There is no pos account code configuration for outlet {} and shift {}".format(self.outlet, self.shift_name))
	
	revenue_data = get_revenues(self)
	
	for d in revenue_data:
		account_code = [x.account_code for x in  config.pos_revenue_account_codes if x.revenue==d["revenue_group"]]
		if not account_code:
			frappe.throw("There is no account code configuration for revenue group {}".format(d["revenue_group"]))
		
		if (d["discount"] or 0)> 0:
			discount_account_code = [x.discount_account for x in  config.pos_revenue_account_codes if x.revenue==d["revenue_group"] and x.discount_account]
			if not discount_account_code:
				frappe.throw("There is no account code confiuration for discount amount of revenue group {}".format(d["revenue_group"]))

	

				
	#tax 1 
	tax_1_amount = sum([d["tax_1_amount"] for d in revenue_data]) or 0
	if tax_1_amount > 0 and not config.tax_1_account:
		frappe.throw("There is no account configuration for Tax 1")
		
	#tax 2 
	tax_2_amount = sum([d["tax_2_amount"] for d in revenue_data]) or 0
	if tax_2_amount > 0 and not config.tax_2_account:
		frappe.throw("There is no account configuration for Tax 2")
	#tax 3 
	tax_3_amount = sum([d["tax_3_amount"] for d in revenue_data]) or 0
	if tax_3_amount > 0 and not config.tax_3_account:
		frappe.throw("There is no account configuration for Tax 3")


	#post payment to folio transaction
	payment_data= get_payments(self)
	for p in payment_data:
		account_code = [x for x in  config.pos_payment_type_account_codes if x.payment_type==p["payment_type"]]
		if not account_code:
			frappe.throw("Payment type {} does not have account code".format(p["payment_type"]))
		
		if (p["fee_amount"] or 0)> 0:
			if not account_code[0].bank_fee_account:
				frappe.throw("There is no account code configuration for bank fee amount of payment type {}".format(p["payment_type"]))
 

@frappe.whitelist()
def submit_pos_data_to_folio_transaction(self):
	account_code_config = frappe.db.get_list("POS Account Code Config", filters={"outlet":self.outlet, "shift_name":self.shift_name})
	config = None
	if account_code_config:
		config =  frappe.get_doc("POS Account Code Config",account_code_config[0].name)
	if not config:
		return
	

	revenue_data = get_revenues(self)
	payment_data= get_payments(self)

	#pos revenue
	discount_data = []
	for d in revenue_data:
		account_code = [x.account_code for x in  config.pos_revenue_account_codes if x.revenue==d["revenue_group"]]
		
		if account_code:
			account_code = account_code[0]
			if (d['sub_total'] or 0 )> 0:
				post_folio_transaction(self,account_code,d['sub_total'] or 0)

		if (d["discount"] or 0)> 0:
			discount_account_code = [x.discount_account for x in  config.pos_revenue_account_codes if x.revenue==d["revenue_group"]]
			if discount_account_code:
				discount_account_code = discount_account_code[0]
				discount_data.append({"account_code":discount_account_code, "discount":d["discount"]})

	

				
	# Discount
	if len(discount_data)>0:
		account_codes = set([d["account_code"] for d in discount_data]) 
		for acc in account_codes:
			post_folio_transaction(self,acc,sum([d['discount'] for d in discount_data if d["account_code"]==acc]))

	#tax 1 
	tax_1_amount = sum([d["tax_1_amount"] for d in revenue_data]) or 0
	if tax_1_amount > 0 and config.tax_1_account:
		post_folio_transaction(self, config.tax_1_account, tax_1_amount)
		
	#tax 2 
	tax_2_amount = sum([d["tax_2_amount"] for d in revenue_data]) or 0
	if tax_2_amount > 0 and config.tax_2_account:
		post_folio_transaction(self, config.tax_2_account, tax_2_amount)
	#tax 3 
	tax_3_amount = sum([d["tax_3_amount"] for d in revenue_data]) or 0
	if tax_3_amount > 0 and config.tax_3_account:
		post_folio_transaction(self, config.tax_3_account, tax_3_amount)


	#post payment to folio transaction
	
	for p in payment_data:
		account_code = [x for x in  config.pos_payment_type_account_codes if x.payment_type==p["payment_type"]]
		if account_code:
			p["account_code"] = account_code[0].account_code
		else:
			frappe.throw("Payment type {} does not have account code".format(p["payment_type"]))
		if (p["fee_amount"] or 0)> 0:
			p["bank_fee_account"] = account_code[0].bank_fee_account

	#post transaction that relate to cashier shift
	# we use set to get unique account code, cause cash $ and cash riel payment type can be post to same account code
	
	for acc in set([a["account_code"] for a in payment_data]):
		post_folio_transaction(self, acc, sum([ (x["amount"] or 0) +  (x["fee_amount"] or 0) for x in payment_data if x['account_code'] == acc]) )
	
	 

	#post bank fee acount
	 
	for acc in set([a["bank_fee_account"] for a in payment_data if "bank_fee_account" in a ]):
		post_folio_transaction(self, acc, sum([x["fee_amount"] for x in payment_data if "bank_fee_account" in x and  x['bank_fee_account'] == acc]) )
	
def post_folio_transaction(self,account_code, amount, folio_transaction_type=None, folio_transaction_number = None):
	 
	frappe.get_doc( 
				{
					'doctype': 'Folio Transaction',
					'property':self.business_branch,
					'working_day':self.working_day,
					'cashier_shift':self.name,
					'posting_date':self.posting_date,
					'transaction_type': folio_transaction_type or  "Cashier Shift",
					'transaction_number': folio_transaction_number or  self.name ,
					'reference_number':folio_transaction_number or self.name,
					"input_amount":amount, 
					"account_code":account_code,
				} 
			).insert(ignore_permissions=True)

def get_revenues(self):
	sql="""select 
			sp.revenue_group,
			sum(sp.sub_total) as sub_total,
			sum(sp.total_discount) as discount,
			sum(sp.tax_1_amount) as tax_1_amount,
			sum(sp.tax_2_amount) as tax_2_amount,
			sum(sp.tax_3_amount) as tax_3_amount
		from `tabSale Product` sp 
		inner join `tabSale` s on s.name = sp.parent
		where
			s.cashier_shift='{}' and 
			s.docstatus=1
		group by 
			sp.revenue_group
		""".format(self.name)
	
	return frappe.db.sql(sql,as_dict=1)
 


 

def get_payments(self):
	sql="""select 
			payment_type,
			sum(payment_amount) as amount,
			sum(fee_amount) as fee_amount
		from `tabSale Payment`
		where
			docstatus=1 and 
			cashier_shift='{0}'
		group by
			payment_type
		""".format(self.name)
	
	return frappe.db.sql(sql,as_dict=1)

