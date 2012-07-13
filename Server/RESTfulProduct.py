import psycopg2, ppygis, psycopg2.extras, json, Exceptions, cherrypy, shutil
from RESTful import RESTResource

class CheckArgs(object):
    
    def __init__(self, vpath_check, params_check):
        self.params = params_check
        self.vpath = vpath_check
        self._wrapped = None

    def __get__(self, obj, type=None):
        self.obj = obj
        return self

    def _shim(self, instance, *args, **kwargs):
        return self._wrapped(instance, *args, **kwargs)
 
    def __call__(self, wrapped):
        self._wrapped = wrapped
        def shim(instance, *args, **kwargs):
            for value in self.params:
                if value not in kwargs.keys():
                    raise Exceptions.LookupError('rest_args_error', 400)
                    
            for value in self.vpath:
                if value not in args.keys():
                    raise Exceptions.LookupError('rest_path_error', 400)
                    
            return self._shim(instance, *args, **kwargs)
        return shim

class Product(RESTResource):

    def handle_GET(self, *vpath, **params):
        return self.process(*vpath, **params)
        
    def handle_POST(self, *vpath, **params):
        return self.process(*vpath, **params)
        
    def process(self, *vpath, **params):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        try:
            print vpath[0] 
            raise Exception("cats")         
    
        except Exceptions.HttpError as e:
            return json.dumps(e.message, sort_keys=True, indent=4)   
        except Exception as e:
            return json.dumps({'code': 405, 'msg':e.message}, sort_keys=True, indent=4)
        
    
