#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from sitewide_settings import DEBUG

import tools

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class FourOhFour(tools.TemplateServingHandler):
	def get(self):
		self.not_found()

def main():
	import pages
	list = []
	pages.add_all(list)
	list.append(('.*', FourOhFour))
	
	application = webapp.WSGIApplication(list,
                                         debug = DEBUG)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
