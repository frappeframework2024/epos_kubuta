# Copyright (c) 2023, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class SaleProductSPACommission(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		business_branch: DF.Data | None
		commission_amount: DF.Currency
		duration: DF.Int
		duration_title: DF.Data | None
		employee: DF.Link | None
		employee_name: DF.Data | None
		is_deleted: DF.Check
		is_overtime: DF.Data | None
		modifiers: DF.SmallText | None
		portion: DF.Data | None
		posting_date: DF.Date | None
		product_name: DF.Data | None
		product_name_kh: DF.Data | None
		sale: DF.Link | None
		sale_product: DF.Link | None
		shift_name: DF.Data | None
	# end: auto-generated types
	pass
