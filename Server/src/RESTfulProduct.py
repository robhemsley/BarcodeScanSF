"""
"""

import json, Exceptions, cherrypy, MySQLdb, MySQLdb.cursors
from RESTful import RESTResource
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

class Product(RESTResource):
    """
    """
    DB_HOST = "sorted.robhemsley.webfactional.com"
    DB_USER = "robhemsley_sf"
    DB_NAME = "robhemsley_sf"
    DB_PASS = "wgpmilo1988"
    
    __INSERT_DATA = ""
    
    def __init__(self, env, variables):
        #super(RESTResource, self).__init__(env, variables)
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
            self._check_gtin(*vpath, **params)
            test = GoogleAPI()
            tmp = self._check_db(self._check_gtin(*vpath, **params))
            if tmp == None:
                data = test.get_product(self._check_country(*vpath, **params), self._check_gtin(*vpath, **params))
                data = data[0]
                
                cursor = self.db.cursor()
                cursor.execute("INSERT INTO Products (Title, Description, Brand, Store, Gtin, URL, Img_URL, Price, Currency, Category) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s')"% (data["title"], data["des"], data["brand"], data["store"], data["gtin"], data["url"], data["img_url"], data["price"], data["currency"], data["category"]))
                self.db.commit()
            else:
                data = tmp[0]
        
            if len(vpath) == 2:
                return json.dumps(self._process_rest(data, ""), indent=4)
            else:
                return json.dumps(self._process_rest(data, vpath[2]), indent=4)
                
            
    
        except Exceptions.HttpError as e:
            return json.dumps(e.message, sort_keys=True, indent=4)   
        except Exception as e:
            return json.dumps({'code': 405, 'msg':e.message}, sort_keys=True, indent=4)
    
    def _process_rest(self, data, req):
        data = dict((k.lower(), v) for k,v in data.iteritems())
        if req == "title":
            return {"title": data["title"]}
        elif req == "url":
            return {"url": data["url"]}
        elif req == "img":
            return {"img": data["img_url"]}
        elif req == "des":
            return {"des": data["des"]}
        elif req == "brand":
            return {"brand": data["brand"]}
        elif req == "store":
            return {"store": data["store"]}
        elif req == "category":
            return {"store": data["category"]}
        elif req == "price":
            return {"price": data["price"], "currency": data["currency"]}         
        else:
            return data
                
                
    def _check_country(self, *vpath, **params):
        if vpath[0] not in COUNTRY_CODES:
            raise Exceptions.RestError("invalid_country", 500)
        return vpath[0]
        
    def _check_gtin(self, *vpath, **params):
        gtin = vpath[1]
        return gtin
    
    def _check_db(self, gtin):
        cursor = self.db.cursor()
        cursor.execute("""SELECT * FROM Products WHERE Gtin = '%s'"""% (gtin.lstrip('0')))
        result = cursor.fetchall()
        if len(result) > 0:
            return result
        else:
            return None
        
        
    
