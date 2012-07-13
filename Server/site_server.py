import cherrypy, jinja2, os, sys
from jinja2 import Environment, PackageLoader
from api import v0

sys.path.append("../")

VARIABLES = {}
ENV = Environment(loader=jinja2.FileSystemLoader(['templates/']))

class API:
	"""
	API - Class
	"""
	
	def __init__(self):
		"""
		__init__ - Method
		"""
		self.v0 = v0(ENV, VARIABLES)

	@cherrypy.expose
	def index(self):
		"""
		index - Method
		"""
		return "API Version required: API/v0/"
	
class Crowd:
	@cherrypy.expose
	def index(self):
		template = ENV.get_template("index.html")
		return template.render()
	
	@cherrypy.expose
	def uploadTest(self):
		template = ENV.get_template("uploadTest.html")
		return template.render()
	
if __name__ == '__main__':
	servRoot = Crowd()
	servRoot.API = API()
	
	tutconf = os.path.join(os.path.dirname(__file__), 'config.conf')
	cherrypy.quickstart(servRoot, config=tutconf)

