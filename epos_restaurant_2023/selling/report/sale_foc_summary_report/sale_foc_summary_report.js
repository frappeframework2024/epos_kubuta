// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sale FOC Summary Report"] = {
	onload: function(report) {
		if(frappe.query_report.get_filter_value('filter_based_on')=="This Month"){

		
			frappe.query_report.toggle_filter_display('from_fiscal_year', true);
			frappe.query_report.toggle_filter_display('start_date', true  );
			frappe.query_report.toggle_filter_display('end_date', true );
		}
		report.page.add_inner_button("Preview Report", function () {
			frappe.query_report.refresh();
		});
	},
	"filters": [
		{
			fieldname: "business_branch",
			label: "Business Branch",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Business Branch', txt);
			},
			"on_change": function (query_report) {},
			 
		},
		{
			"fieldname":"filter_based_on",
			"label": __("Filter Based On"),
			"fieldtype": "Select",
			"options": ["Fiscal Year","This Month", "Date Range"],
			"default": ["This Month"],
			"reqd": 1,
			on_change: function() {
				let filter_based_on = frappe.query_report.get_filter_value('filter_based_on');
				if(filter_based_on!="This Month"){ 
					frappe.query_report.toggle_filter_display('from_fiscal_year', filter_based_on === 'Date Range');
					frappe.query_report.toggle_filter_display('start_date', filter_based_on === 'Fiscal Year'  );
					frappe.query_report.toggle_filter_display('end_date', filter_based_on === 'Fiscal Year' );

				
				}else{
					frappe.query_report.toggle_filter_display('from_fiscal_year', true);
					frappe.query_report.toggle_filter_display('start_date', true  );
					frappe.query_report.toggle_filter_display('end_date', true );

				}
	 
			}
		},
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
	
			"reqd": 1,
			"on_change": function (query_report) {},
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
		
			"reqd": 1,
			"on_change": function (query_report) {},
		},
		{
			"fieldname":"from_fiscal_year",
			"label": __("Start Year"),
			"fieldtype": "Int",
			
			"default": (new Date()).getFullYear(),
			"on_change": function (query_report) {},
			hide_in_filter:1,
		},
		{
			"fieldname": "pos_profile",
			"label": __("POS Profile"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('POS Profile', txt);
			},
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "outlet",
			"label": __("Outlet"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Outlet', txt);
			},
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "product_group",
			"label": __("Product Group"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				
				return frappe.db.get_link_options('Product Category', txt,{"is_group":1});
			},
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "product_category",
			"label": __("Product Category"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				group = frappe.query_report.get_filter_value("product_group");
				if(group==""){
					return frappe.db.get_link_options('Product Category', txt,filters={
						is_group:0
					});
				}
				else {
					return frappe.db.get_link_options('Product Category', txt,filters={
						is_group:0,
						"parent_product_category":["in",group]
					});
				}
			},
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "customer_group",
			"label": __("Customer Group"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				
				return frappe.db.get_link_options('Customer Group', txt);
			},
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options":"Customer",
			"on_change": function (query_report) {},
			
		},
		{
			"fieldname": "parent_row_group",
			"label": __("Parent Group By"),
			"fieldtype": "Select",
			"options": "\nCategory\nProduct Group\nRevenue Group\nBusiness Branch\nOutlet\nTable Group\nTable\nPOS Profile\nCustomer\nCustomer Group\nStock Location\nDate\n\Month\nYear\nSale Invoice\nWorking Day\nCashier Shift\nSale Type",
			"on_change": function (query_report) {},
			hide_in_filter:1,
		},
		{
			"fieldname": "row_group",
			"label": __("Row Group By"),
			"fieldtype": "Select",
			"options": "Product\nCategory\nProduct Group\nRevenue Group\nBusiness Branch\nOutlet\nTable Group\nTable\nPOS Profile\nCustomer\nCustomer Group\nStock Location\nDate\n\Month\nYear\nSale Invoice\nWorking Day\nCashier Shift\nSale Type",
			"default":"Category",
			"on_change": function (query_report) {},
			hide_in_filter:1,
		},
		{
			"fieldname": "column_group",
			"label": __("Column Group By"),
			"fieldtype": "Select",
			"options": "None\nDaily\nWeekly\nMonthly\nQuarterly\nHalf Yearly\nYearly",
			"default":"None",
			"on_change": function (query_report) {},
			hide_in_filter:1,
		},
		{
			"fieldname": "hide_columns",
			"label": __("Hide Columns"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return [
					{"value":"Quantity","description":"Quantity"},
					{"value":"Sub Total","description":"Sub Total"},
					{"value":"Discount","description":"Discount"},
					{"value":"Tax","description":"Tax"},
					{"value":"Cost","description":"Cost"},
					{"value":"Profit","description":"Pofit"}
				]
			},
			"on_change": function (query_report) {},
			hide_in_filter:1,
		},
		{
			"fieldname": "chart_type",
			"label": __("Chart Type"),
			"fieldtype": "Select",
			"options": "None\nbar\nline\npie",
			"default":"bar",
			"on_change": function (query_report) {},
			hide_in_filter:1,
		},
		{
			"fieldname": "show_summary",
			"label": __("Show Summary"),
			"fieldtype": "Check",
			default:true,
			hide_in_filter:1,
			"on_change": function (query_report) {},
		},

	],
	"formatter": function(value, row, column, data, default_formatter) {
	
		value = default_formatter(value, row, column, data);

		if (data && data.is_group==1) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "bold");
			

			value = $value.wrap("<p></p>").parent().html();
		}
		
		return value;
	},
};
