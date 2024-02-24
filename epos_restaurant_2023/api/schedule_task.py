import functools
import re
import json
from datetime import datetime, timedelta
import frappe
from frappe import _

@frappe.whitelist()
def generate_audit_trail_from_version():
    audit_trail_documents = frappe.db.get_list("Audit Trail Document", pluck='name',filters={"is_epos_audit_trail":1})
    version_data = frappe.db.get_list('Version',
                        filters={
                            'ref_doctype': ["in",audit_trail_documents],
                            "custom_is_converted_to_audit_trail":0
                        },
                        fields=['name','ref_doctype', 'docname',"creation"],
                        page_length=20
                    )
    # return version_data
    if len(version_data)> 0:
        for v in version_data:
            
            if frappe.db.exists(v.ref_doctype, v.docname):
                doc = frappe.get_doc("Version", v.name)

                submit_update_audit_trail_from_version(doc)
        
        #update is converted
        frappe.db.sql("update `tabVersion` set custom_is_converted_to_audit_trail=1 where name in %(names)s", {"names":[d.name for d in version_data]})
        frappe.db.commit()
        return version_data

def update_audit_trail_from_version(doc, method=None, *args, **kwargs):    
    if frappe.db.exists("Audit Trail Document",doc.ref_doctype,cache=True):
        submit_update_audit_trail_from_version(doc)
        # frappe.enqueue("edoor.api.utils.submit_update_audit_trail_from_version", queue='short', doc=doc)

def submit_update_audit_trail_from_version(doc):
    if frappe.db.exists("Audit Trail Document",doc.ref_doctype,cache=True):
        doctype = frappe.get_doc("Audit Trail Document", doc.ref_doctype)
        data = json.loads(doc.data)
        data_changed = []

        for d in data["changed"]:
            if d[0] in [f.field_name for f in doctype.tracking_field] and ((d[1] or '')!='' or (d[2] or '')!=''):
                field = [f  for f in doctype.tracking_field if f.field_name==d[0]][0]

                if field.field_type=="Check":
                    data_changed.append(f'<b>{field.label}</b>: {"Yes" if d[1]==1 else "No"} <b>to</b> {"Yes" if d[2]==1 else "No"}')
                elif field.field_name == 'docstatus':
                    _from = "Draft"                    
                    if d[1] == 0:
                        _from = _from
                    elif d[1] == 1:
                        _from = "Submited"
                    elif d[1] == 2: 
                        _from = "Cancelled"

                    _to = "Draft"
                    if d[2] == 0:
                        _to = _to
                    elif d[2] == 1:
                        _to = "Submited"
                    elif d[2] == 2: 
                        _to = "Cancelled"
                    data_changed.append(f'<b>{field.label}</b>: {_from} <b>to</b> {_to}')

                elif 'tax_' in field.field_name:
                    ref_doc = frappe.get_doc(doc.ref_doctype,doc.docname)
                    if field.field_name == 'tax_1_rate':
                        data_changed.append(f'<b>{ref_doc.tax_1_name}</b>: {d[1]}% <b>to</b> {d[2]}%')
                    elif field.field_name == 'tax_1_amount':
                        data_changed.append(f'<b>{ref_doc.tax_1_name} Amount </b>: {d[1]} <b>to</b> {d[2]}')
                    elif field.field_name == 'tax_2_rate':
                        data_changed.append(f'<b>{ref_doc.tax_2_name}</b>: {d[1]}% <b>to</b> {d[2]}%')
                    elif field.field_name == 'tax_2_amount':
                        data_changed.append(f'<b>{ref_doc.tax_2_name} Amount </b>: {d[1]} <b>to</b> {d[2]}')
                    elif field.field_name == 'tax_2_rate':
                        data_changed.append(f'<b>{ref_doc.tax_2_name}</b>: {d[1]}% <b>to</b> {d[2]}%')
                    
                    elif field.field_name == 'tax_3_rate':
                        data_changed.append(f'<b>{ref_doc.tax_3_name}</b>: {d[1]}% <b>to</b> {d[2]}%')
                    elif field.field_name == 'tax_3_amount':
                        data_changed.append(f'<b>{ref_doc.tax_3_name} Amount </b>: {d[1]} <b>to</b> {d[2]}')
                
                else:
                    if field.hide_old_value==1:
                        data_changed.append(f'<b>{field.label}</b>: {d[2]}')
                    else:
                        data_changed.append(f'<b>{field.label}</b>: {d[1]} <b>to</b> {d[2]}')


        if len(data_changed)>0:
            comment_doc = []
            comment_doc.append({
            "creation":doc.creation,
            "subject": "Change Value",
            "custom_audit_trail_type":"Updated",
            "custom_icon":"pi pi-file-edit",
            "reference_doctype":doc.ref_doctype,
            "reference_name":doc.docname,
            "content":", ".join(data_changed)  
            })
            # frappe.enqueue("edoor.api.utils.add_audit_trail", queue='long', data=comment_doc)
            add_audit_trail(comment_doc, update_creation_date=True)


    
def add_audit_trail(data,update_creation_date=False):
    for d in data:    
        if frappe.db.exists(d["reference_doctype"],d["reference_name"]):
            doc = frappe.get_doc(d["reference_doctype"],d["reference_name"])
            # d["custom_posting_date"] = datetime.now()
            if d["reference_doctype"] in ["Membership","Membership Payment"]:
                d["custom_posting_date"]= doc.posting_date
            else:
                d["custom_posting_date"] = datetime.now()


        d["doctype"]="Comment"
        if not hasattr(d,"comment_type"):
            d["comment_type"]="Info"
            
        d["custom_is_audit_trail"]=1
        d["comment_by"]:frappe.session.user.full_name

        doc = frappe.get_doc(d).insert(ignore_permissions=True)
        if update_creation_date:
            frappe.db.sql("update `tabComment` set creation=%(creation)s where name=%(name)s",{"name":doc.name, "creation":d["creation"]})

