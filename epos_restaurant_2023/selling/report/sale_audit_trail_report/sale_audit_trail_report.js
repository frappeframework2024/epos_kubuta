// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.query_reports["Sale Audit Trail Report"] = {
	"filters": [
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"on_change": function (query_report) { },
			"reqd": 1
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"on_change": function (query_report) { },
			"reqd": 1
		},
		{
			"fieldname": "subject",
			"label": __("Subject"),
			"fieldtype": "MultiSelectList",
			"on_change": function (query_report) { },
			get_data: function(txt) {
				return [
					{"value":"Create New Sale","description":"Create New Sale"},
					{"value":"New Sale Item","description":"New Sale Item"},
					{"value":"Append Quantity","description":"Append Quantity"},
					{"value":"Change Price","description":"Change Price"},
					{"value":"Change Quantity","description":"Change Quantity"},
					{"value":"Free Sale Product","description":"Free Sale Product"},
					{"value":"Remove Free Sale Product","description":"Remove Free Sale Product"},
					{"value":"Discount Sale Product","description":"Discount Sale Product"},
					{"value":"Remove Discount Sale Product","description":"Remove Discount Sale Product"},
					{"value":"Delete Sale Product","description":"Delete Sale Product"},
					{"value":"Delete Not Submit Sale Product","description":"Delete Not Submit Sale Product"},
					{"value":"Sale Discount","description":"Sale Discount"},
					{"value":"Cancel Discount Sale","description":"Cancel Discount Sale"},
					{"value":"Quick Payment","description":"Quick Payment"},
					{"value":"Payment","description":"Payment"},
					{"value":"Print Bill","description":"Print Bill"},
					{"value":"Cancel Print Bill","description":"Cancel Print Bill"},
					{"value":"Edit Bill","description":"Edit Bill"},
					{"value":"Delete sale order","description":"Delete sale order"},
				]
			},
		},
		{
			"fieldname": "select_user",
			"label": __("Select User"),
			"fieldtype": "Link",
			"options":"User",
			"on_change": function (query_report){}
		},
	],
	onload: function (report) {  
		report.page.add_inner_button("Preview Report", function () {
			report.refresh();
		});		
	},
};
