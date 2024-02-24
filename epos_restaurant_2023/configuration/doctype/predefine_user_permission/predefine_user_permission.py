# Copyright (c) 2024, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PredefineUserPermission(Document):
	def before_save(self):
		users = frappe.db.get_list("User",filters={
        	'role_profile_name': self.role_profile
    	})
		for user in users:
			for user_permission in self.permissions:
				exist = frappe.db.exists("User Permission",{ "allow": user_permission.allow,'for_value':user_permission.for_value,'user':user})
				frappe.throw(exist)
				if exist:
					frappe.delete_doc('Task', exist)
				frappe.get_doc({
					'doctype': 'User Permission',
					'user':user,
					'allow':user_permission.allow,
					'for_value':user_permission.for_value,
					'hide_descendants':user_permission.hide_descendants,
					'apply_to_all_doctypes':user_permission.apply_to_all_document_types
				}).insert(ignore_if_duplicate=True)
