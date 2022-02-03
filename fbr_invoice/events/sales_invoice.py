import frappe
from frappe import _
import json
import requests
from pyqrcode import create as qrcreate

@frappe.whitelist()
def send_pos_invoice_fbr(doc=None, handler=None):
    try:
        doc = frappe._dict(json.loads(doc))
        # login to system
        # print orgid
        # loginurl = 'http://192.168.0.176:8524/api/IMSFiscal/Get'


        item_list = []
        for item in doc.get("items"):
            item = frappe._dict(item)
            item_list.append({
                "ItemCode": item.item_code,
                "ItemName": item.item_name,
                "Quantity": item.qty,
                "PCTCode": "",
                "TaxRate": 0,
                "SaleValue": item.rate,
                "TotalAmount": item.amount,
                "TaxCharged": 0,
                "Discount": "0.0",
                "FurtherTax": 0,
                "InvoiceType": 1,
                "RefUSIN": None
            })

        data = {
            "InvoiceNumber": "",
            "POSID": doc.pos_id,
            "USIN": "SALE\/POS\/BEVERLY\/2021\/05\/100361",
            "DateTime": doc.posting_date,
            "BuyerNTN": doc.ntn_no,
            "BuyerCNIC": None,
            "BuyerName": doc.customer,
            "BuyerPhoneNumber": None,
            "TotalBillAmount": doc.net_total,
            "TotalQuantity": 7,
            "TotalSaleValue": doc.grand_total,
            "TotalTaxCharged": "0",
            "Discount": "0",
            "FurtherTax": "0",
            "PaymentMode": 1,
            "RefUSIN": None,
            "InvoiceType": 1,
            "Items": item_list
        }
        
        data = json.dumps(data)

        """
            COMMENT FOR TESTING END
        """

        url = 'http://127.0.0.1:8524/api/IMSFiscal/GetInvoiceNumberByModel'

        response = requests.post(url, data=data, headers={
            'content-type': "application/json"
        })

        print(response)
        res_data = json.loads(response.content)

        print(res_data)

        """
            COMMENT FOR TESTING END
        """

        frappe.db.set_value(doc.doctype, doc.name, "fbr_invoice_no", res_data["InvoiceNumber"])
        # frappe.db.set_value(doc.doctype, doc.name, "fbr_invoice_no", "12345")
        generate_fbr_barcode(res_data["InvoiceNumber"])
        # generate_fbr_barcode("12345")
        frappe.db.commit()
        return res_data["InvoiceNumber"]
    except Exception as ex:
        print(ex)
        return ex

@frappe.whitelist()
def set_invoice_number(doctype, name, inv):
    frappe.db.set_value(doctype, name, "fbr_invoice_no", inv)
    generate_fbr_barcode(inv, name)
    frappe.db.commit()

@frappe.whitelist()
def generate_fbr_barcode(code=None, docname=None):
    from pathlib import Path
    import os
    import qrcode

    try:
        name_tobe = docname + ".png"
        # Get the current working directory
        cwd = os.getcwd()
        print(cwd)
        f = open(cwd+"/currentsite.txt", "r")
        currentsitename = f.readline()
        check_file = Path(cwd + "/" + currentsitename + "/public/files/qrcodes/" + name_tobe)
        if not check_file.is_file():
            img = qrcode.make(code)
            img.save(cwd + "/" + currentsitename + '/public/files/qrcodes/' + name_tobe)
    except Exception as ex:
        print(ex)