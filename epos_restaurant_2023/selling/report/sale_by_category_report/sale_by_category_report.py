# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe

value_fields = (
	"qty",
	"sub",
	"disc",
	"total",
)

def execute(filters=None):
	
	return get_columns(filters), get_report_data(filters)

def get_columns(filters):
	return [
		{"fieldname":"name", "label": "Product Category", "width":250,"fieldtype":"Data"},
		{"fieldname":"qty", "label": "QTY", "width":90,"fieldtype":"Data"},
		{"fieldname":"sub", "label": "Sub Total", "width":125,"fieldtype":"Currency"},
		{"fieldname":"disc", "label": "Discount", "width":125,"fieldtype":"Currency"},
		{"fieldname":"total", "label": "Total Amount", "width":125,"fieldtype":"Currency"},
	]

def get_report_data(filters):
	category_filter=""
	category_filter_list=[]
	if filters.product_category:
		lft_rgt = frappe.db.sql("""select min(lft) lft,max(rgt) rgt from `tabProduct Category` where name = '{}'""".format(filters.product_category),as_dict=True)[0]
		category_filter = """ and a.product_category in(select name from `tabProduct Category` where lft >= {0} and rgt <= {1})""".format(lft_rgt["lft"],lft_rgt["rgt"])
		category_filter_list = frappe.db.sql("""select name from `tabProduct Category` where lft >= {0} and rgt <= {1}""".format(lft_rgt["lft"],lft_rgt["rgt"]),as_dict=True)
	sale_data = frappe.db.sql("""
						SELECT 
						    a.product_category,
							SUM(a.quantity) qty,
							SUM(a.sub_total) sub,
							SUM(a.discount_amount) disc,
							SUM(a.amount) total
						from `tabSale Product` a
						INNER JOIN `tabSale` b ON b.name = a.parent
						where b.posting_date between '{0}' and '{1}' and a.docstatus=1 and b.docstatus=1 {2}
						GROUP BY product_category""".format(filters.start_date,filters.end_date,category_filter),as_dict=True)
	
	if len(sale_data)<=0:
		return
	product_categories = frappe.db.sql("select name,parent_product_category from `tabProduct Category`",as_dict=True)
	product_categories = prepared_category(product_categories)
	data = prepare_data(product_categories,sale_data)
	category_by_name = prepared_category_by_name(data)
	accumulate_values_into_parents(data,category_by_name)
	filtered_data = []
	if filters.product_category :
		for a in category_filter_list:
			for b in data:
				if a["name"] == b["name"]:
					filtered_data.append(b)
	else:
		filtered_data = data
	
	total_qty=0;total_sub=0;total_disc=0;total_amt=0
	for a in sale_data:
		total_qty+=a.qty
		total_sub+=a.sub
		total_disc+=a.disc
		total_amt+=a.total
	row = {"name": "Total","parent_product_category":None,"indent": 0,"qty": total_qty,"sub": total_sub,"disc": total_disc,"total": total_amt,"sort_order":10000000}
	filtered_data.append(row)
	return sorted(filtered_data, key=lambda x: x["sort_order"], reverse=False)

def prepared_category(product_categories, depth=20):
	parent_children_map = {}
	for d in product_categories:
		parent_children_map.setdefault(d.parent_product_category or None, []).append(d)

	filtered_categories = []

	def add_to_list(parent, level):
		if level < depth:
			children = parent_children_map.get(parent) or []
			for child in children:
				child.indent = level
				filtered_categories.append(child)
				add_to_list(child.name, level + 1)

	add_to_list(None, 0)
	index = 0
	for a in filtered_categories:
		a["sort_order"] = index
		index = index + 1
	return filtered_categories

def prepared_category_by_name(product_categories, depth=20):
	category_by_name = {}
	for d in product_categories:
		category_by_name[d["name"]] = d
	return category_by_name


def prepare_data(product_categories,sale_data):
	data = []
	for d in product_categories:
		qtys = [a for a in sale_data if a.product_category == d.name]
		qty = 0;sub = 0;disc=0;total=0
		if qtys:
			qty = qtys[0].qty
			sub = qtys[0].sub
			disc = qtys[0].disc
			total = qtys[0].total
		row = {
			"name": d.name,
			"parent_product_category": d.parent_product_category,
			"indent": d.indent,
			"qty": qty,
			"sub": sub,
			"disc": disc,
			"total": total,
			"sort_order":d.sort_order
		}
		data.append(row)
	return data

def accumulate_values_into_parents(product_categories, category_by_name):
	for d in reversed(product_categories):
		if d["parent_product_category"]:
			for key in value_fields:
				category_by_name[d["parent_product_category"]][key] += d[key]

def get_list(filters,name):
	data = ','.join("'{0}'".format(x.replace("'", "''")) for x in filters.get(name))
	return data