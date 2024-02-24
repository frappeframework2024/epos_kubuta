// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.query_reports["Membership Register Report"] = {
	"filters": [
		{
			"fieldname":"start_date",
			"label": __("Register (Start Date)"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),	
			"on_change": function (query_report) { },		 
			"reqd": 1
		},
		{
			"fieldname":"end_date",
			"label": __("Register (End Date)"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"on_change": function (query_report) { },
			"reqd": 1
		},
		{
			"fieldname": "customer",
			"label": __("Member"),
			// "fieldtype": "Link",
			// "options":"Customer",
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Customer', txt);
			},
			"on_change": function (query_report) { },
			
		},
		{
			"fieldname": "personal_trainer",
			"label": __("Trainer"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Trainer', txt);
			},
			"on_change": function (query_report) { },
			
		},
		{
			"fieldname": "sort_by",
			"label": __("Sort By"),
			"fieldtype": "Select",
			"options": "Member Code\nMember\nRegister Date",
			"default":"Register Date",
			"on_change": function (query_report) { },
		},
		{
			"fieldname": "sort_type",
			"label": __("Sort Type"),
			"fieldtype": "Select",
			"options": "ASC\nDESC",
			"default":"ASC"		,
			"on_change": function (query_report) { },
		},
		{
			"fieldname": "is_all_transaction",
			"label": __("All Transaction"),
			"fieldtype": "Check",
			"default":"0"		,
			"on_change": function (query_report) { 
				let is_all_transaction = query_report.get_filter_value('is_all_transaction');
				query_report.toggle_filter_display('end_date', is_all_transaction === 1 );
				query_report.toggle_filter_display('start_date', is_all_transaction === 1 );				
			}, 
		},
		{
			"fieldname": "is_none_trainer",
			"label": __("None Trainer"),
			"fieldtype": "Check",
			"default":"0"		,
			"on_change": function (query_report) { 
				let is_none_trainer = query_report.get_filter_value('is_none_trainer');
				query_report.toggle_filter_display('personal_trainer', is_none_trainer === 1 );			
			}, 
		},
		{
			"fieldname": "group_by_reference_no",
			"label": __("Group By Reference No"),
			"fieldtype": "Check",
			"default":"0"		,
			"on_change": function (query_report) { }, 
		}
	],
	onload: function (report) {
		let is_all_transaction = report.get_filter_value('is_all_transaction');
		if(is_all_transaction==0){
			report.toggle_filter_display('end_date', false );
			report.toggle_filter_display('start_date', false);
		}else{
			
			report.toggle_filter_display('end_date', true );
			report.toggle_filter_display('start_date', true);
		}
		
		let is_none_trainer = report.get_filter_value('is_none_trainer'); 
		if(is_none_trainer==0){
			report.toggle_filter_display('personal_trainer', false );	
		}else{
			report.toggle_filter_display('personal_trainer',true );	
		}


		report.page.add_inner_button("Preview Report", function () {
			report.refresh();
		});
		
	},
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


