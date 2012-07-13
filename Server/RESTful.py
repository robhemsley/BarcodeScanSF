import cherrypy, Exceptions, psycopg2

class RESTResource(object):
    
    db_conn = None
    db_cursor = None
    db_username = "robhemsley_crowd"
    db_password = "wgpmilo1988"
    db_host = "robhemsley.webfactional.com"
    
    __CHECK_USR_DEV = "SELECT \"Password\" FROM \"Owner\", \"Devices\" WHERE \"email\" = '%s' AND \"Owner\".\"ID\" = \"Devices\".\"Owner_id\" AND \"Password\" = md5('%s') AND \"Devices\".\"Device_id\" = '%s'"
    __CHECK_USR_LOGIN = "SELECT \"Password\" FROM \"Owner\" WHERE \"email\" = '%s' AND \"Password\" = md5('%s')"
    __GET_DEV_ID = "SELECT * FROM \"Devices\" WHERE \"Device_id\" = '%s'"   
    
    def __init__(self, env, variables):
        self.__db_connect()
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
    
    def __db_connect(self):
        """
        __db_connect - Method
            Connects to the objects specified database
        """
        if not self.__check_db_connection():
            self.db_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"% (self.db_username, self.db_username, self.db_host, self.db_password))
            self.db_cursor = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
 
    def __check_db_connection(self):
        """
        __check_db_connection - Method
            Checks that the current local database cursor is currently connected to the
            remote database.
            
        @return: Boolean value indicating if there is a current database connection
        @rtype: Boolean
        """
        try:
            self.db_cursor.execute("SELECT 1")
        except Exception:
            return False
        else:
            return True  
    
    def check_login(self, email, password, exception = False):
        """
        check_login - Method
        """
        self.db_cursor.execute(self.__CHECK_USR_LOGIN% (email, password))
        if len(self.db_cursor.fetchall()) == 0:
            if exception: 
                raise Exceptions.AuthError('login_failed', 500)
            return False
        else:
            return True
        
    def check_login_device(self, email, password, device_id, exception = False):
        """
        check_login - Method
        """
        print self.__CHECK_USR_DEV% (email, password, device_id)
        self.db_cursor.execute(self.__CHECK_USR_DEV% (email, password, device_id))
        tmp = self.db_cursor.fetchall()
        print len(tmp)
        if len(tmp) == 0:
            if exception: 
                raise Exceptions.AuthError('login_failed', 500)
            return False
        else:
            return True
        
    def check_device_id(self, device_id, exception = False):
        """
        check_device_id - Method
        """
        self.db_cursor.execute(self.__GET_DEV_ID% (device_id))
        
        if len(self.db_cursor.fetchall()) == 0:
            if exception: 
                raise Exceptions.LookupError('device_not_found', 500)
            return False
        else:
            return True
        
        
        
        
        
        