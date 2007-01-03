import pkg_resources
pkg_resources.require("TurboGears")

import cherrypy
import turbogears

turbogears.update_config(modulename="turbocare.config")
turbogears.update_config(configfile="/home/devv/svn/turbocare/prod.cfg")

from turbocare.controllers import Root

cherrypy.root = Root()
cherrypy.server.start(initOnly=True, serverClass=None)   

def fixuphandler(req):
    return 0
