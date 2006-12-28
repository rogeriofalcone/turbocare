import logging
import cherrypy
import turbogears
from turbogears import controllers, expose, validate, redirect
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model
import model_userperm
import controllers_his
import controllers_inventory
import controllers_billing
import controllers_registration
import controllers_dispensing
import controllers_store
import controllers_reports
import controllers_UDReport	
import controllers_saved_reports
from turbocare import json

log = logging.getLogger("turbocare.controllers")

class Root(controllers.RootController):
     #catwalk = CatWalk(model,allowedHosts=['127.0.0.1','192.168.11.3','192.168.11.120'])
    catwalk = CatWalk(model_userperm) #Create a user admininstrator CatWalk with the custom User Model.
    catwalk = identity.SecureObject(catwalk,identity.in_group('admin'))  #Securing objects is good. 
	
    billing = controllers_billing.Billing()
    billing = identity.SecureObject(billing,identity.has_permission('bill_view'))
	
    saved = controllers_saved_reports.SavedReport()
    
    his = controllers_his.HIS()
    
    
    inventory = controllers_inventory.Inventory()
    inventory = identity.SecureObject(inventory,identity.in_group('admin'))
    
	
    registration = controllers_registration.Registration()
    registration = identity.SecureObject(registration,identity.has_permission('reg_view'))
    
    reports = controllers_reports.Reports()
    user_reports = controllers_UDReport.UserDefinedReport()
    
    # Dispensing locations
    warehouse_main = identity.SecureObject(controllers_dispensing.Dispensing(1) ,identity.has_permission('warehouse_main_view'))
    pharmacy_main = identity.SecureObject(controllers_dispensing.Dispensing(2), identity.has_permission('pharmacy_main_view')) # id=2 is Pharmacy Main 


    # xray = controllers_dispensing.Dispensing(9) # id=9 is the xray dept.
    
    # Store locations - Warehouse managing tools
    warehouse_store = identity.SecureObject(controllers_store.Store(1, "warehouse_store"),identity.has_permission('warehouse_store_view'))   
    pharmacy_store = identity.SecureObject(controllers_store.Store(2, "pharmacy_store"),identity.has_permission('pharmacy_store_view'))
 
    
    @expose(template="turbocare.templates.welcome")
    def index(self):
        import time
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(now=time.ctime())

    @expose(template="turbocare.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):
        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)
        forward_url=None
        previous_url= cherrypy.request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= cherrypy.request.headers.get("Referer", "/")
        cherrypy.response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=cherrypy.request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")

    @expose(format='json')
    def LoadMenu(self, **kw):
        '''	Return a list of menu items available to the current user
        '''
        log.debug('....Loading menu')
        results = []

        #Display top menu based on permissions of user. 
        if identity.has_permission("reg_view"):    
            results.append(dict(link='/registration',name='Registration'))
        if identity.has_permission("bill_view"):
            results.append(dict(link='/billing',name='Billing'))
        if identity.has_permission("pharmacy_main_view"):
            results.append(dict(link='/pharmacy_main',name='Pharmacy dispensing'))
        if identity.has_permission("warehouse_main_view"):
            results.append(dict(link='/warehouse_main',name='Warehouse dispensing'))    
        if identity.has_permission("pharmacy_store_view"):
            results.append(dict(link='/pharmacy_store',name='Pharmacy Inventory'))
        if identity.has_permission("warehouse_store_view"):
            results.append(dict(link='/warehouse_store',name='Warehouse Inventory'))            
        if identity.in_group("admin"):
            results.append(dict(link='/inventory',name='Admin Inventory'))
            results.append(dict(link='/catwalk',name='User admin'))

        return dict(results=results)
