"""
"""

import json, Exceptions, cherrypy, MySQLdb, MySQLdb.cursors
from RESTful import RESTResource
from RESTfulProduct import Product
from services.GoogleAPI import GoogleAPI

COUNTRY_CODES = {"UK": {"Name": "United Kingdom", "Currency": "GBP"}, 
                 "US": {"Name": "United States Of America", "Currency": "USD"}}

class CheckArgs(object):
    """
    """
    
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
                if value not in args:
                    raise Exceptions.LookupError('rest_path_error', 400)
                    
            return self._shim(instance, *args, **kwargs)
        return shim

class Find(RESTResource):
    """
    """
    DB_HOST = "sorted.robhemsley.webfactional.com"
    DB_USER = "robhemsley_sf"
    DB_NAME = "robhemsley_sf"
    DB_PASS = "wgpmilo1988"
    
    __INSERT_DATA = ""
    
    def __init__(self, env, variables):
        #super(RESTResource, self).__init__(env, variables)
        self.Product = Product(env, variables)

        self.db = MySQLdb.connect(host= self.DB_HOST,
                     user= self.DB_USER,
                     passwd= self.DB_PASS,
                     db= self.DB_NAME, 
                     cursorclass=MySQLdb.cursors.DictCursor)
    
    def handle_GET(self, *vpath, **params):
        return self.process(*vpath, **params)
        
    def handle_POST(self, *vpath, **params):
        return self.process(*vpath, **params)
        
    def process(self, *vpath, **params):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        
        
        try:
            data = params['gtin'].split(",")
            for gtin in data:
                print self.Product.process_gtin(gtin, "UK")
                results = self._check_db(self.Product.process_gtin(gtin, "UK")['Title'])
                print results
                print "cat"
                output = []
                for result in results:
                    result.pop("Timestamp")
                    output.append(result)
                
            return json.dumps(output, indent=4)  
                    
        except Exceptions.HttpError as e:
            return json.dumps(e.message, sort_keys=True, indent=4)   
        except Exception as e:
            return json.dumps({'code': 405, 'msg':e.message}, sort_keys=True, indent=4)
    
    def _check_db(self, title):
        cursor = self.db.cursor()
        cursor.execute("""SELECT * FROM `Recipe` WHERE `Recipe`.`ID` = (SELECT `Recipe_ID` FROM `Ingredient` WHERE `Item_ID` = (SELECT `ID` FROM `Item` WHERE LOCATE(`Name`, "%s") > 0 LIMIT 0,1) LIMIT 0,1)"""% (title))
        result = cursor.fetchall()
        return result
        
        
    
