import frappe
from frappe.utils import date_diff,today 
from frappe.utils.data import strip
import datetime


def execute(filters=None):
	if filters.filter_based_on =="Fiscal Year":
		if not filters.from_fiscal_year:
			filters.from_fiscal_year = datetime.date.today().year
		
		filters.start_date = '{}-01-01'.format(filters.from_fiscal_year)
		filters.end_date = '{}-12-31'.format(filters.from_fiscal_year) 

	validate(filters)
	#run this to update parent_product_group in table sales invoice item

	report_data = []
	skip_total_row=False
	message=None
	report_data = get_report_data(filters)  
 
	return get_columns(filters), report_data, message, None, None,skip_total_row
 

def validate(filters):
	if filters.start_date and filters.end_date:
		if filters.start_date > filters.end_date:
			frappe.throw("The 'Start Date' ({}) must be before the 'End Date' ({})".format(filters.start_date, filters.end_date))

def get_columns(filters):
	columns = []
	columns.append({'fieldname':'row_group','label':"Date",'fieldtype':'Data','align':'left','width':250})

	for c in get_dynamic_columns(filters):
		columns.append(c)

	return columns

def get_dynamic_columns(filters):
	#dynmic report file
	columns = []	
	payment_types = frappe.db.get_list("Payment Type",filters=[{"payment_type_group":['!=', "On Account"]},{"disabled":0}],order_by='sort_order asc')
	for p in payment_types:
		columns.append({
					"label":p.name,
					"fieldname":"{}".format(p.name.replace(" ", "_").lower()), 
					"fieldtype":"Float",
					"align":"center",
					})
		
	columns.append({
					"label":"Total Payment",
					"fieldname":"total_payment", 
					"fieldtype":"Currency",
					"align":"center"
					})
	return columns


def get_report_data(filters):
	row_group = [d["fieldname"] for d in get_row_groups() if d["label"]=='Date'][0]
 
	sql = "select {} as row_group ".format(row_group) + ", "
	sql = sql + get_report_field_by_payment_type(filters)	
	sql =sql + """ 
		FROM `tabMembership Payment` AS a
		WHERE
			a.docstatus = 1 and
			{0}
		GROUP BY 
		{1}
	""".format(get_conditions(filters),row_group)	
	
	data = frappe.db.sql(sql,filters, as_dict=1)
	
	return data

def get_report_field_by_payment_type(filters ):
	payment_types = frappe.db.get_list("Payment Type")
	sqls=[]
	for p in payment_types:
		payment_type = p.name.replace("-"," ")
		payment_type = payment_type.replace("(", "_")
		payment_type = payment_type.replace(")", "_")
		payment_type = payment_type.replace(" ", "_")
		sqls.append("ifnull(sum(if(a.payment_type='{0}',a.input_amount,0)),0) as {1}".format(p.name,payment_type.lower()))
		sqls.append("ifnull(sum(if(a.payment_type='{0}',a.input_amount/a.exchange_rate,0)),0) as base_{1}".format(p.name,payment_type.lower()))
        

	sqls.append("ifnull(sum(a.payment_amount),0) as total_payment")
	return  ','.join(sqls)
 

def get_conditions(filters):
	conditions = " 1 = 1 "

	start_date = filters.start_date
	end_date = filters.end_date
	conditions += " AND a.posting_date between '{}' AND '{}'".format(start_date,end_date)
	
	return conditions


def get_row_groups():
	return  [
		{
			"fieldname":"date_format(a.posting_date,'%%Y/%%m/%%d')",
			"label":"Date",
			"parent_row_group_filter_field":"row_group"
		}
	]