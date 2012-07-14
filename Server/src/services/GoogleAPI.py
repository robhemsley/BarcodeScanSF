import json
from BaseService import BaseService

"""
Created on Jul 13, 2012

@author: Rob
"""

class GoogleAPI(BaseService):
    """
    classdocs
    """
    API_KEY = "AIzaSyAjNzASWkwaoQ8vnQs56FTvu-MtFaNWRAM"
    BASE_URL = "https://www.googleapis.com/shopping/search/v1/public/products?maxResults=1&country=%(country_code)s&q=%(gtin)s&key=" + API_KEY

    def __init__(self):
        """
        Constructor
        """
        
    def _api_call(self, variables):
        products = json.loads(self._http_get(self.BASE_URL% (variables)))
        if products["totalItems"] == 0:
            raise Exception("Product Not Found") 
        
        output = []
        for product in products["items"]:
            output.append(product["product"])
            
        return output
    
    def get_product(self, country_code, gtin):
        output = []
        for product in self._api_call({"country_code": country_code, "gtin": gtin}):
            product_dict = {}
            
            if "description" in product:
                product_dict["description"] = product["description"]
            else:
                product_dict["description"] = "None"
                
            if "title" in product:
                product_dict["title"] = product["title"]
            else:
                product_dict["title"] = "None
                
            if "brand" in product:
                product_dict["brand"] = product["brand"]    
            else:
                product_dict["brand"] = "None"           
                
            if "author" in product:
                if "name" in product["author"]:
                    product_dict["store"] = product["author"]["name"]
                else:
                    product_dict["store"] = "None"
            else:
                product_dict["store"] = "None                    
                       
            if "gtin" in product:
                product_dict["gtin"] = product["gtin"].lstrip('0')
            else:
                product_dict["gtin"] = "None"   
                  
            if "images" in product:
                product_dict["img_url"] = product["images"][0]["link"] 
            else:
                product_dict["img_url"] = "None"   
                       
            if "link" in product:
                product_dict["url"] = product["link"]      
            else:
                product_dict["url"] = "None"
                  
            if "inventories" in product:
                product_dict["price"] = product["inventories"][0]["price"]    
                product_dict["currency"] = product["inventories"][0]["currency"]
            else:
                product_dict["price"] = "None"   
                product_dict["currency"] = "None"   
                
            product_dict["category"] = "None"   
                
            output.append(product_dict)
        
        return output
        
        
if __name__ == "__main__":
    hmm = GoogleAPI()
    print hmm.get_product("US", "50251414")
