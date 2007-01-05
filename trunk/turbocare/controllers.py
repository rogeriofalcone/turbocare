import logging
import cherrypy
import turbogears
from turbogears import controllers, expose, validate, redirect
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model
import model_userperm
import controllers_inventory
import controllers_billing
import controllers_registration
import controllers_dispensing
import controllers_store
import controllers_reports
import controllers_UDReport	
import controllers_saved_reports
import controllers_configuration
import controllers_user_manager
from turbocare import json

log = logging.getLogger("turbocare.controllers")

class Root(controllers.RootController):
	
    def __init__(self):
	    # Dynamically create Store and dispensing locations from locations which we have in the database
	    Locations = model.InvLocation.select()
	    for location in Locations:
		    name_store = '%s_store' % location.Name.lower().replace(' ','_')
		    name_disp = '%s_disp' % location.Name.lower().replace(' ','_')
		    log.debug("Current location is " + str(location))
		    # Create the store location
		    if getattr(self,name_store,None) == None:
			    setattr(self,name_store,eval('identity.SecureObject(controllers_store.Store(%d, "%s"),identity.has_permission("%s_view"))' % (location.id, name_store, name_store)))
		    # Create the dispensing location
		    if location.CanSell:
			    if getattr(self,name_disp,None) == None:
				    setattr(self,name_disp,eval('identity.SecureObject(controllers_dispensing.Dispensing(%d),identity.has_permission("%s_view"))' % (location.id, name_disp)))
	    
     #catwalk = CatWalk(model,allowedHosts=['127.0.0.1','192.168.11.3','192.168.11.120'])
    catwalk = CatWalk(model_userperm) #Create a user admininstrator CatWalk with the custom User Model.
    catwalk = identity.SecureObject(catwalk,identity.has_permission('admin_catwalk'))  #Securing objects is good. 
    #tempwalk = CatWalk(model_userperm) #Create a user admininstrator CatWalk with the custom User Model.
    user_manager = controllers_user_manager.UserManager()
    billing = controllers_billing.Billing()
    billing = identity.SecureObject(billing,identity.has_permission('bill_view'))
	
    saved = controllers_saved_reports.SavedReport()
    configuration = identity.SecureObject(controllers_configuration.Configuration(),identity.has_permission('admin_controllers_configuration'))
    
    inventory = controllers_inventory.Inventory()
    inventory = identity.SecureObject(inventory,identity.has_permission('admin_controllers_inventory'))
    
	
    registration = controllers_registration.Registration()
    registration = identity.SecureObject(registration,identity.has_permission('reg_view'))
    
    reports = controllers_reports.Reports()
    user_reports = controllers_UDReport.UserDefinedReport()
    
    # Dispensing locations
    # warehouse_main = identity.SecureObject(controllers_dispensing.Dispensing(1) ,identity.has_permission('warehouse_main_view'))
    # pharmacy_main = identity.SecureObject(controllers_dispensing.Dispensing(2), identity.has_permission('pharmacy_main_view')) # id=2 is Pharmacy Main 
    # Store locations - Warehouse managing tools
    # warehouse_store = identity.SecureObject(controllers_store.Store(1, "warehouse_store"),identity.has_permission('warehouse_store_view'))   
    # pharmacy_store = identity.SecureObject(controllers_store.Store(2, "pharmacy_store"),identity.has_permission('pharmacy_store_view'))
	
    
    @expose(template="turbocare.templates.welcome")
    def index(self):
        import time
	if identity.current.anonymous:
		raise redirect("/login")
        log.debug("Crazy TurboGears Controller Responding For Duty")
        return dict(now=time.ctime(),menuitems=self.UserMenu())

    @expose(template="turbocare.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):
        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            if forward_url in ['',None,'/login','login']:
		    raise redirect('/')
            else:
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
        raise redirect("/login")

    @expose(format='json')
    def LoadMenu(self, **kw):
        '''	Return a list of menu items available to the current user
        '''
        return dict(results=self.UserMenu())

    def UserMenu(self, **kw):
        '''	Return a list of menu items available to the current user
        '''
        log.debug('UserMenu')
        results = []
        #Display top menu based on permissions of user. 
	if identity.not_anonymous():
		results.append(dict(link='/user_reports',name='User Reports',sub_menu=[]))
        if identity.has_permission("reg_view"):    
            results.append(dict(link='/registration',name='Registration',sub_menu=[]))
        if identity.has_permission("bill_view"):
            results.append(dict(link='/billing',name='Billing',sub_menu=[]))
        Locations = model.InvLocation.select()
	LocationStoreGroups = {}
	LocationDispGroups = {}
        for location in Locations:
	    name_store = '%s_store' % location.Name.lower().replace(' ','_')
	    name_disp = '%s_disp' % location.Name.lower().replace(' ','_')
	    # Create the store link
	    if getattr(self,name_store,None) != None and identity.has_permission('%s_view' % name_store):
		    for group in location.Groups:
			    if LocationStoreGroups.has_key(group.Name):
				    LocationStoreGroups[group.Name].append(dict(link='/%s' % name_store, name='%s Inventory' % location.Name,sub_menu=[]))
			    else:
				    LocationStoreGroups[group.Name] = [dict(link='/%s' % name_store, name='%s Inventory' % location.Name,sub_menu=[])]
		    if len(location.Groups) == 0:
			    if LocationStoreGroups.has_key('Other'):
				    LocationStoreGroups['Other'].append(dict(link='/%s' % name_store, name='%s Inventory' % location.Name,sub_menu=[]))
			    else:
				    LocationStoreGroups['Other'] = [dict(link='/%s' % name_store, name='%s Inventory' % location.Name,sub_menu=[])]
	    # Create the dispensing location
	    if location.CanSell:
		    if getattr(self,name_disp,None) != None and identity.has_permission('%s_view' % name_disp):
			    for group in location.Groups:
				    if LocationDispGroups.has_key(group.Name):
					    LocationDispGroups[group.Name].append(dict(link='/%s' % name_store, name='%s Dispensing' % location.Name,sub_menu=[]))
				    else:
					    LocationDispGroups[group.Name] = [dict(link='/%s' % name_store, name='%s Dispensing' % location.Name,sub_menu=[])]
			    if len(location.Groups) == 0:
				    if LocationDispGroups.has_key('Other'):
					    LocationDispGroups['Other'].append(dict(link='/%s' % name_store, name='%s Dispensing' % location.Name,sub_menu=[]))
				    else:
					    LocationDispGroups['Other'] = [dict(link='/%s' % name_store, name='%s Dispensing' % location.Name,sub_menu=[])]
        if len(LocationStoreGroups) > 0:
		SubMenu = []
		keys = LocationStoreGroups.keys()
		keys.sort()
		for key in keys:
			SubMenu.append(dict(link='',name=key, sub_menu=LocationStoreGroups[key]))
		results.append(dict(link='', name='Inventory', sub_menu=SubMenu))
        if len(LocationDispGroups) > 0:
		SubMenu = []
		keys = LocationDispGroups.keys()
		keys.sort()
		for key in keys:
			SubMenu.append(dict(link='',name=key, sub_menu=LocationDispGroups[key]))
		results.append(dict(link='', name='Dispensing', sub_menu=SubMenu))
        if identity.has_permission("admin_controllers_inventory"):
            results.append(dict(link='/inventory',name='Admin Inventory',sub_menu=[]))
        if identity.has_permission("admin_catwalk"):
            results.append(dict(link='/catwalk',name='User admin',sub_menu=[]))
        if identity.has_permission("admin_controllers_configuration"):
            results.append(dict(link='/configuration',name='Configuration Admin',sub_menu=[]))
        return results
