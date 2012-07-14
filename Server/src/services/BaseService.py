"""
Created on Jul 13, 2012

@author: Rob
"""

import httplib2, urllib, urllib2, poster, cookielib

class BaseService(object):
    """
    classdocs
    """


    def __init__(self ):
        """
        Constructor
        """
        
    def _http_get(self, url):
        """
        """
        http = httplib2.Http()
        response, content = http.request(url, 'GET')
        if response["status"] == "200":
            return content
        else:
            raise Exception("Test")