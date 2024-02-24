import frappe
import shutil
def before_migrate ():
    frappe_path = frappe.utils.get_bench_path()
    shutil.copy2(frappe_path + '/' + 'apps/epos_restaurant_2023/epos_restaurant_2023/print_template/print_grid.html', frappe_path + '/' + 'apps/frappe/frappe/public/js/frappe/views/reports/print_grid.html')

    shutil.copy2(frappe_path + '/' + 'apps/epos_restaurant_2023/epos_restaurant_2023/print_template/query_report.js', frappe_path + '/' + 'apps/frappe/frappe/public/js/frappe/views/reports/query_report.js')

    shutil.copy2(frappe_path + '/' + 'apps/epos_restaurant_2023/epos_restaurant_2023/print_template/print_grid.html', frappe_path + '/' + 'sites/assets/frappe/js/frappe/views/reports/print_grid.html')

    shutil.copy2(frappe_path + '/' + 'apps/epos_restaurant_2023/epos_restaurant_2023/print_template/query_report.js', frappe_path + '/' + 'sites/assets/frappe/js/frappe/views/reports/query_report.js')


    #copy file file from 
    
    # Source : 
    #apps/epos_restaurant_2023/epos_restaurant_2023/print_template/print_grid.html
    #apps/epos_restaurant_2023/epos_restaurant_2023/print_template/query_report.js

    #destination 1
    #apps/frappe/frappe/public/js/frappe/views/reports/print_grid.html
    #apps/frappe/frappe/public/js/frappe/views/reports/query_report.js

    #destination 2
    #sites/assets/frappe/js/frappe/views/reports/print_grid.html
    #sites/assets/frappe/js/frappe/views/reports/query_report.js

    pass
    
def after_migrate():
    frappe.db.sql("update `tabSale` set total_paid_with_fee = total_paid + total_fee where total_paid_with_fee <> total_paid + total_fee")
    
    # frappe.db.sql("delete from `tabPrint Format` where name in ('Sale','Sale Receipt Test','Close Sale Summary','Close Sale Summary - UI') and standard='Yes'")
    # frappe.db.sql("delete from `tabUnit of Measurement Conversion` where name in ('e7c28b72f2')")
    # frappe.db.sql("delete from `tabPrinter` where printer_name in ('Kitchen Printer','Cashier Printer', 'Bar Printer')")




    
    
    