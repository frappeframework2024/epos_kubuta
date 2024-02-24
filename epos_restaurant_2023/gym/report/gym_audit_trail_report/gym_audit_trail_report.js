// Copyright (c) 2024, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.query_reports["GYM Audit Trail Report"] = {
	"filters": [
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"reqd": 1,
			"on_change": function (query_report){}
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"reqd": 1,
			"on_change": function (query_report){}
		},
		{
			"fieldname":"select_filter",
			"label": __("Select Filter"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return [
					{"value":"Membership","description":"Membership",fieldtype:"Data"},
					{"value":"Membership Payment","description":"Membership Payment",fieldtype:"Data"},
				]
			},
			"on_change": function (query_report){}
		},
		{
			"fieldname": "select_user",
			"label": __("Select User"),
			"fieldtype": "Link",
			"options":"User",
			"on_change": function (query_report){}
		},
		{
			"fieldname": "order_by_audit",
			"label": __("Order By"),
			"fieldtype": "Select",
			"options": "Last Update On\nCreated On\nAudit Date\nReference Document\nReference Name\nSubject\nDescription\nCreated By",
			default:"Last Update On",
			hide_in_filter:1,
			"on_change": function (query_report){}
		},
		{
			"fieldname": "sort_order",
			"label": __("Sort Order"),
			"fieldtype": "Select",
			"options": "ASC\nDESC",
			default:"ASC",
			hide_in_filter:1,
			"on_change": function (query_report){}
		},
	],
	onload: function (report) { 

		report.page.add_inner_button("Preview Report", function () {
			report.refresh();
		});
		
	},
	
};
