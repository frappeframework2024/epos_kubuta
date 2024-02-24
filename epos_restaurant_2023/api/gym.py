import json
import time
import frappe
import base64
from py_linq import Enumerable
from frappe.utils import today, add_to_date
from datetime import datetime, timedelta
import calendar
from dateutil import relativedelta
from frappe import _


@frappe.whitelist()
def membership_check_in(code,check_in_date):  
    check_member = frappe.db.exists("Customer",code) 
    if not check_member:
        return False

    cus = frappe.get_doc("Customer",code)
    member = {
        "name":cus.name,
        "customer_code_name":cus.customer_code_name,
        "customer_name_en":cus.customer_name_en,
        "customer_name_kh":cus.customer_name_kh,
        "customer_group":cus.customer_group,
        "date_of_birth":cus.date_of_birth,
        "gender":cus.gender,
        "phone_number":cus.phone_number,
        "photo":cus.photo
    }
    data_membership = frappe.db.get_list("Membership",fields=[ "name","docstatus"], filters=[{'customer':code},{'docstatus':1}])
    
    membership_family = frappe.db.sql("select member,parent from `tabMembership Family` where member = '{}' and docstatus = 1".format(code),as_dict=1)
    if len(membership_family) > 0:
        _data_membership = frappe.db.get_list("Membership",fields=[ "name","docstatus"], filters=[{'name':membership_family[0].parent},{'docstatus':1}])
        for d in _data_membership:
            data_membership.append(d)

    memberships =[]
    for child in data_membership:
        m = frappe.get_doc("Membership",child.name)
        locked = False
        
        if m.access_type != "Unlimited":
            access = {
                "per_duration":m.per_duration,
                "access_type":m.access_type,
                "duration":m.duration
            }
            locked =  check_access_to_train(access,check_in_date,code,m)
        
        ## get total checked in  
        sql = """select count(`name`) as total_check_in from `tabMembership Check In Items` 
					where  membership = '{}' 
					and docstatus = 1 """.format( m.name)	
        
 
        exec = frappe.db.sql(sql, as_dict=1)
        count = 0
        if exec:
            count = (exec[0].total_check_in or 0)
            if m.tracking_limited == 1:
                locked = True if count >= m.max_access else locked

        memberships.append({   
            "name":m.name,           
            "duration_type":m.duration_type,
            "membership_duration":m.membership_duration,
            "membership":m.membership,
            "membership_type":m.membership_type,
            "duration_base_on":m.duration_base_on,
            "posting_date":m.posting_date,
            "start_date":m.start_date,
            "end_date":m.end_date,
            "access_type":m.access_type,
            "duration":m.duration,
            "per_duration":m.per_duration,
            "selected":False,
            "locked":locked,
            "total_checked_in":count,
            "tracking_limited":m.tracking_limited,
            "max_access":m.max_access
        })
 
    data = {
        'check_in_date':check_in_date,
        'member':member,
        'membership':memberships
    }
    return data


@frappe.whitelist()
def check_access_to_train(access,check_in_date,code,membership):
    m = membership
    locked = False
    query = """select
                COUNT(DISTINCT a.membership) as count_check_in
            from `tabMembership Check In Items` as a 
            inner join `tabMembership Check In` as b on b.name = a.parent
            where b.docstatus = 1 
                and a.docstatus = 1
                and a.membership = '{}' """.format(m.name)
   
    date_format = '%Y-%m-%d'
    match access['per_duration']:
        case "Day":
            con = query + " and b.check_in_date = '{}'".format(check_in_date)
           
 
            data_query = frappe.db.sql(con,as_dict=1) 
            if data_query: 
                if data_query[0].count_check_in >= access['duration']:
                    locked = True               
                    
       
        case "Week":
            # end_date = datetime.strptime(check_in_date,date_format)
            # start_date = end_date + timedelta(days=-6) # Subtracting 6 days.
            # start_date_formatted = start_date.strftime(date_format)
            # con = " between '{}' and '{}'".format(start_date_formatted,end_date)
            # query.format(con,code,m.name)
            # data_query = frappe.db.sql(query,as_dict=1) 

            # if data_query:
            #     if data_query[0].count_check_in >= access['duration']:
            #         locked = True 
            pass                    

        case "Month":
            # end_date = datetime.strptime(check_in_date,date_format)
            # start_date = end_date + relativedelta.relativedelta(months=-1) # Subtracting 1 month.
            # start_date = start_date + timedelta(days=1) # add 1 days.
            # start_date_formatted = start_date.strftime(date_format)

            # con = " between '{}' and '{}'".format(start_date_formatted,end_date)
            # query.format(con,code,m.name)
            # data_query = frappe.db.sql(query,as_dict=1) 

            # if data_query:
            #     if data_query[0].count_check_in >= access['duration']:
            #         locked = True

            pass

        case "Year":
            # end_date = datetime.strptime(check_in_date,date_format)
            # start_date = end_date + relativedelta.relativedelta(years=-1) # Subtracting 1 month.
            # start_date = start_date + timedelta(days=1) # add 1 days.
            # start_date_formatted = start_date.strftime(date_format)

            # con = " between '{}' and '{}'".format(start_date_formatted,end_date)
            # query.format(con,code,m.name)
            # data_query = frappe.db.sql(query,as_dict=1) 

            # if data_query:
            #     if data_query[0].count_check_in >= access['duration']:
            #         locked = True
            pass   
            
        case _:
            locked = False

    return locked





@frappe.whitelist()
def check_in_submit_data(data):   
    values = json.loads(data)    
    for d in values:
        doc = frappe.get_doc(d)
        doc.insert()

        #submit doctype
        doc.submit()
    frappe.db.commit()  
    return doc


@frappe.whitelist()
def get_recent_checked_ins(limit=15):
    date_format = '%Y-%m-%d'
    today = datetime.today().strftime(date_format)
    query = """select 
        i.name,
        m.name as membership_check_in,
        concat(m.member,'-', m.member_name) as member_name, 
        m.photo,
        m.check_in_date, 
        i.creation, 
        i.membership,
        i.membership_name,
        i.membership_type ,
        i.check_in_number
    from `tabMembership Check In Items` i 
    inner join `tabMembership Check In` m on m.name = i.parent  
    where m.docstatus = 1 and i.docstatus = 1
    and m.check_in_date = '{}'
    order by i.creation desc limit {}""".format(today,limit)
    docs = frappe.db.sql(query,as_dict=1)
    return docs


## get trainer link option report
@frappe.whitelist()
def get_trainer_link_option(name):
    data = frappe.db.get_list("Trainer",fields=["name","trainer_name_en","trainer_name_kh","phone_number"])
    if data:
        result = []
        for d in data:
            name = d.trainer_name_en if d.trainer_name_kh == d.trainer_name_en else '{}-{}'.format(d.trainer_name_kh,d.trainer_name_en)
            description = name
            if d.phone_number:
                description = '{}, {}'.format(name,d.phone_number)
            result.append({"value":d.name,'label':d.trainer_name_en,"description": description})
        return result
    return None