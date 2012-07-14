"""
"""

import cherrypy, Exceptions

class RESTResource(object):
    """
    """
    
    def __init__(self, env, variables):
        self.env = env
        self.variables = variables
        
    @cherrypy.expose
    def default(self, *vpath, **params):
        """
        default - Method
        """
        method = getattr(self, "handle_" + cherrypy.request.method, None)
        if not method:
            methods = [x.replace("handle_", "")
            for x in dir(self) if x.startswith("handle_")]
            cherrypy.response.headers["Allow"] = ",".join(methods)
            raise cherrypy.HTTPError(405, "Method not implemented.")
        
        return method(*vpath, **params);
        
        
        
        
        