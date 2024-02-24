// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.query_reports["Membership Payment Report"] = {
	"filters": [
		{
			"fieldname":"filter_based_on",
			"label": __("Filter Based On"),
			"fieldtype": "Select",
			"options": ["Fiscal Year", "Date Range"],
			"default": ["Fiscal Year"],
			"reqd": 1, 
			on_change: function() {	 
				let filter_based_on = frappe.query_report.get_filter_value('filter_based_on');
				frappe.query_report.toggle_filter_display('from_fiscal_year', filter_based_on === 'Date Range');
				frappe.query_report.toggle_filter_display('start_date', filter_based_on === 'Fiscal Year');
				frappe.query_report.toggle_filter_display('end_date', filter_based_on === 'Fiscal Year');
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"hidden": 1,
			"reqd": 1
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"hidden": 1,
			"reqd": 1
		},
		{
			"fieldname":"from_fiscal_year",
			"label": __("Start Year"),
			"fieldtype": "Int",			
			"default": (new Date()).getFullYear()
		}
	],
	onload(frm){
		let filter_based_on = frappe.query_report.get_filter_value('filter_based_on');
		frappe.query_report.toggle_filter_display('from_fiscal_year', filter_based_on === 'Date Range');
		frappe.query_report.toggle_filter_display('start_date', filter_based_on === 'Fiscal Year');
		frappe.query_report.toggle_filter_display('end_date', filter_based_on === 'Fiscal Year');
		frappe.query_report.refresh();
    },
};
