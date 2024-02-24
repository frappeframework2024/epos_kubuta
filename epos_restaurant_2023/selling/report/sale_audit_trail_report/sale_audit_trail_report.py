
import frappe
from frappe import _
from frappe.utils import date_diff,today ,add_months, add_days
from frappe.utils.data import getdate, strip
import datetime
import uuid
from dateutil.rrule import rrule, MONTHLY
from datetime import datetime
import copy
import calendar


def execute(filters=None):
	report_data = get_report_data(filters)
	return get_columns(filters),report_data,None,None, None


def get_columns(filters):
	columns = [
		{'fieldname':'posting_date','fieldtype':'Date','align':'left','label':'Posting Date',"width":110 ,"show_in_report":1},
		{'fieldname':'audit_date','fieldtype':'Date','align':'left','label':'Audit Date',"width":110 ,"show_in_report":1},
		{'fieldname':'creation','fieldtype':'Time','align':'left','label':'Time',"width":95 ,"show_in_report":1},
		{'fieldname':'reference_name','align':'left','label':'Ref Name #','fieldtype':'Link','options':'Sale',"width":150 ,"show_in_report":1},
		{'fieldname':'custom_bill_number','align':'left','label':'Bill No#',"width":150 ,"show_in_report":1},
		{'fieldname':'subject','align':'left','label':'Subject',"width":150 ,"show_in_report":1},
		{'fieldname':'item_desciption','align':'left','label':'Item Description',"width":350 ,"show_in_report":1},
		{'fieldname':'amount','align':'left','label':'Amount','fieldtype':'Currency',"width":100 ,"show_in_report":1},
		{'fieldname':'note','align':'left','label':'Note',"width":350 ,"show_in_report":1},
		{'fieldname':'content','align':'left','label':'Content',"width":500 ,"show_in_report":1},
		{'fieldname':'comment_by','align':'left','label':'By',"width":150 ,"show_in_report":1},
		# {'fieldname':'modified','align':'left','fieldtype':'Datetime','label':'Date & Time',"width":200 ,"show_in_report":1},
	]
	return columns

def get_filters(filters):
	sql = " "

	if filters.subject:
		sql += " and c.`subject` in %(subject)s"
	if filters.select_user:
		sql += " and c.`comment_email` = %(select_user)s"
	sql += " and cast(c.creation as date) between %(start_date)s and %(end_date)s"
	return sql

def get_report_data(filters):
	sql="""select 
			s.posting_date,
			c.reference_name,
			coalesce(s.custom_bill_number,'-') as custom_bill_number,
			c.subject, 
			c.creation,
			c.custom_item_description as item_desciption,
			cast(c.creation as date) as audit_date, 
			c.modified , 
			c.comment_by,
			c.content,
			c.custom_note as note ,
			c.custom_amount as amount
		from `tabComment` c
		left JOIN `tabSale` s on c.reference_name = s.name
		where c.reference_doctype ='Sale' and c.comment_type = 'Info' 
		{}
		order by 
			c.creation desc,
			coalesce(s.custom_bill_number,'-')	desc,
			c.reference_name desc
		""".format(get_filters(filters))
	
	data =  frappe.db.sql(sql,filters,as_dict=1)
	return data