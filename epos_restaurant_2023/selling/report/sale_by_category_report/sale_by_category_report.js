// Copyright (c) 2024, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Sale By Category Report"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"on_change": function (query_report) { }
		},
		{
			"fieldname": "end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"on_change": function (query_report) { }
		},
		{
			"fieldname": "product_category",
			"label": __("Product Category"),
			"fieldtype": "Link",
			"options": "Product Category",
			"get_query": function() {
				return {
					"doctype": "Product Category"
				}
			},
			"on_change": function (query_report) { }
		},
	],
	"tree": true,
	onload: function (report) {
		report.page.add_inner_button("Preview Report", function () {
			frappe.query_report.refresh();
		});
	},
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if ((data && !data.parent_product_category)) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	},
};
