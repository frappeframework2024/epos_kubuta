# Copyright (c) 2023, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class eMenu(WebsiteGenerator):
	def get_context(self, context):
		
		filter={}
		filter["pos_menu"] = [d.menu for d in self.pos_menu_selections]
		data = []
		if filter["pos_menu"]:
			sql ="""
				select 
					name,
					pos_menu,
					product_code,
					product_name_en,
					product_name_kh,
					price,
					ifnull(photo,'files/no_image.jpg') as photo
				from `tabTemp Product Menu`
				where pos_menu in %(pos_menu)s
			"""
			data = frappe.db.sql(sql,filter,as_dict=1)
		context.no_cache = not  (self.enable_cache or 0)
		context.products = data
