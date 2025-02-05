import frappe
from frappe import _
from frappe.utils import cint, cstr
from frappe.auth import LoginManager

@frappe.whitelist()
def get_items():
    items = frappe.get_all('Item', fields=['name', 'item_code', 'item_name', 'item_group', 'stock_uom'])
    return items

@frappe.whitelist()
def add_item(item_code, item_name, item_group, stock_uom):
    try:
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": item_name,
            "item_group": item_group,
            "stock_uom": stock_uom
        })
        item.insert()
        frappe.db.commit()
        return {"success": True, "message": "Item added successfully"}
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": str(e)}




@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
        
        user = frappe.get_doc('User', frappe.session.user)
        return {
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'language': user.language,
                'time_zone': user.time_zone
            },
            'message': _('Logged In')
        }
    except frappe.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response.http_status_code = 401
        return {'success': False, 'message': _('Authentication Failed')}

@frappe.whitelist()
def logout():
    frappe.local.login_manager.logout()
    frappe.db.commit()
    return {'success': True, 'message': _('Logged out')}

@frappe.whitelist()
def get_user_profile():
    user = frappe.get_doc('User', frappe.session.user)
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
        'language': user.language,
        'time_zone': user.time_zone
    }

@frappe.whitelist()
def get_items():
    items = frappe.get_all('Item', fields=['name', 'item_code', 'item_name', 'item_group', 'stock_uom'])
    return items

@frappe.whitelist()
def add_item(item_code, item_name, item_group, stock_uom):
    try:
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": item_name,
            "item_group": item_group,
            "stock_uom": stock_uom
        })
        item.insert()
        frappe.db.commit()
        return {"success": True, "message": "Item added successfully"}
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": str(e)}

