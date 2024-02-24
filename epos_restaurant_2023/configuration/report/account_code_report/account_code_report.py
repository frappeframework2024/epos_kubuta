# Copyright (c) 2023, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	
	return get_report_column(), get_report_data(filters)

def get_report_column():
	return [
		{"fieldname":"name", "label":"Account Code", "fieldtype":"Link","options":"Account Code"},
		{"fieldname":"account_name", "label":"Account Name", "width":200},
		{"fieldname":"type", "label":"Type"},
		{"fieldname":"account_category", "label":"Category"},
		{"fieldname":"price", "label":"Price","fieldtype":"Currency"},
		{"fieldname":"allow_discount", "label":"Allow Dis.", "fieldtype":"Check"},
		{"fieldname":"discount_account", "label":"Dis. Account","width":200},
		{"fieldname":"tax_rule", "label":"Tax Rule","fieldtype":"Link","options":"Tax Rule"},
	]

def get_report_data(filters):
	sql="""select 
				name,
				account_name,
				type,
				parent_account_code,
				allow_discount,
				account_category,
				price,
				concat(discount_account,'-',discount_account_name) as discount_account,
				tax_rule
			from `tabAccount Code` 
			order by 
			sort_order
	"""

	data = frappe.db.sql(sql,as_dict=1)
	report_data = []
	
	for l1 in [x for x in data if x["parent_account_code"]=='All Account Code']:
		report_data.append({"indent":0, "name":l1["name"],"account_name":l1["account_name"]})
		for l2 in [y for y in data if y["parent_account_code"] == l1["name"] ]:
			l2["indent"] = 1
			report_data.append({"indent":1, "name":l2["name"],"account_name":l2["account_name"]})
			for l3 in [z for z in data if z["parent_account_code"] == l2["name"] ]:
				l3["indent"] = 2
				report_data.append(l3)

	


	return report_data



	return data