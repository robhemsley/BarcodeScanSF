import json
import xml.dom.minidom
from BaseService import BaseService

"""
Created on Jul 13, 2012

@author: Rob
"""

class ShopSavvyAPI(BaseService):
    """
    classdocs
    """
    BASE_URL = "http://data.shopsavvy.com/products/%(gtin)s"

    def __init__(self):
        """
        Constructor
        """
        
    def _api_call(self, variables):
        dom = xml.dom.minidom.parseString(self._http_get(self.BASE_URL% (variables)))
        output = []
        try:
            product = {}
            node = dom.documentElement
            product["img_url"] = node.getElementsByTagName('imageUrl')[0].childNodes[0].data
            product["category"] = node.getElementsByTagName('productType')[0].childNodes[0].data
            product["gtin"] = node.getElementsByTagName('productid')[0].childNodes[0].data
            product["title"] = node.getElementsByTagName('title')[0].childNodes[0].data
            output.append(product)
        except Exception:
            raise Exception("Product Not Found") 
        
        return output
    
    def get_product(self, country_code, gtin):
        output = []
        for product in self._api_call({"country_code": country_code, "gtin": gtin}):
            product_dict = {}
                
            if "title" in product:
                product_dict["title"] = product["title"]
            else:
                product_dict["title"] = None                  
                       
            if "gtin" in product:
                product_dict["gtin"] = product["gtin"]  
            else:
                product_dict["gtin"] = None   
                  
            if "images" in product:
                product_dict["img_url"] = product["images"][0]["link"] 
            else:
                product_dict["img_url"] = None   
                
            if "category" in product:
                product_dict["category"] = product["category"]  
            else:
                product_dict["category"] = None 
                       
            product_dict["url"] = None     
            product_dict["price"] = None   
            product_dict["currency"] = None   
            product_dict["brand"] = None           
            product_dict["des"] = None
            product_dict["store"] = None  
                
            output.append(product_dict)
            
        return output
        
        
if __name__ == "__main__":
    hmm = ShopSavvyAPI()
    print hmm.get_product("US", "50251414")
