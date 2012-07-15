"""
"""

from RESTfulProduct import Product
from RESTfulFind import Find

import cherrypy
    
class v0:

    def __init__(self, env, variables):
        self.env = env
        self.variables = variables
        self.Product = Product(env, variables)    
        self.Find = Find(env, variables)

    @cherrypy.expose
    def index(self):
        return "APT Root - Echo Service echo?"
    
    @cherrypy.expose
    def echo(self, **kwargs):
        if cherrypy.request.method in ("POST", "PUT") and cherrypy.request.headers['content-type'].lower() == "application/json":
            json_string = cherrypy.request.body.read()

            return json_string
        else:
            output = ""
            for key in kwargs:
                output += "%s=%s "% (key, kwargs[key])
            
            return output
