# Copyright (c) 2024, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json, os
from frappe.utils.jinja import validate_template
from frappe.modules.utils import export_module_json, get_doc_module

class TestDevTemplate(Document):
	def on_update(self):
		path = export_module_json(self, self.is_standard, self.module)
		if path:
			# js
			if not os.path.exists(path + ".md") and not os.path.exists(path + ".html"):
				with open(path + ".md", "w") as f:
					f.write(self.message)

			# py
			if not os.path.exists(path + ".py"):
				with open(path + ".py", "w") as f:
					f.write(
						"""from __future__ import unicode_literals

	import frappe

	def get_context(context):
	# do your magic here
	pass
	"""
					)