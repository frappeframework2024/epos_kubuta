// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.query_reports["Account Code Report"] = {
	"filters": [

	],
	"formatter": function(value, row, column, data, default_formatter) {
	
		value = default_formatter(value, row, column, data);

		if (data && (data.indent==0 || data.indent==1)) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "bold");
			

			value = $value.wrap("<p></p>").parent().html();
		}
		
		return value;
	},
};
