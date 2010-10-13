import os, logging

APPLICATION_ROOT_DIRECTORY = os.path.dirname(__file__)

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from django.utils import simplejson as json

import UserDict
from Cookie import BaseCookie
class Cookies(UserDict.DictMixin):
    def __init__(self,handler,**policy):
        self.response = handler.response
        self._in = handler.request.cookies
        self.policy = policy
        if 'secure' not in policy and handler.request.environ.get('HTTPS', '').lower() in ['on', 'true']:
            policy['secure']=True
        self._out = {}
    def __getitem__(self, key):
        if key in self._out:
            return self._out[key]
        if key in self._in:
            return self._in[key]
        raise KeyError(key)
    def __setitem__(self, key, item):
        self._out[key] = item
        self.set_cookie(key, item, **self.policy)
    def __contains__(self, key):
        return key in self._in or key in self._out
    def keys(self):
        return self._in.keys() + self._out.keys()
    def __delitem__(self, key):
        if key in self._out:
            del self._out[key]
            self.unset_cookie(key)
        if key in self._in:
            del self._in[key]
            p = {}
            if 'path' in self.policy: p['path'] = self.policy['path']
            if 'domain' in self.policy: p['domain'] = self.policy['domain']
            self.delete_cookie(key, **p)
    #begin WebOb functions
    def set_cookie(self, key, value='', max_age=None,
                   path='/', domain=None, secure=None, httponly=False,
                   version=None, comment=None):
        """
        Set (add) a cookie for the response
        """
        cookies = BaseCookie()
        cookies[key] = value
        for var_name, var_value in [
            ('max-age', max_age),
            ('path', path),
            ('domain', domain),
            ('secure', secure),
            ('HttpOnly', httponly),
            ('version', version),
            ('comment', comment),
            ]:
            if var_value is not None and var_value is not False:
                cookies[key][var_name] = str(var_value)
            if max_age is not None:
                cookies[key]['expires'] = max_age
        header_value = cookies[key].output(header='').lstrip()
        self.response.headers._headers.append(('Set-Cookie', header_value))
    def delete_cookie(self, key, path='/', domain=None):
        """
        Delete a cookie from the client.  Note that path and domain must match
        how the cookie was originally set.
        This sets the cookie to the empty string, and max_age=0 so
        that it should expire immediately.
        """
        self.set_cookie(key, '', path=path, domain=domain,
                        max_age=0)
    def unset_cookie(self, key):
        """
        Unset a cookie with the given name (remove it from the
        response).  If there are multiple cookies (e.g., two cookies
        with the same name and different paths or domains), all such
        cookies will be deleted.
        """
        existing = self.response.headers.get_all('Set-Cookie')
        if not existing:
            raise KeyError(
                "No cookies at all have been set")
        del self.response.headers['Set-Cookie']
        found = False
        for header in existing:
            cookies = BaseCookie()
            cookies.load(header)
            if key in cookies:
                found = True
                del cookies[key]
            header = cookies.output(header='').lstrip()
            if header:
                self.response.headers.add('Set-Cookie', header)
        if not found:
            raise KeyError(
                "No cookie has been set with the name %r" % key)
    #end WebOb functions

class TemplateServingHandler(webapp.RequestHandler):
	def cookies(self):
		try:
			self._ilabs_cookies
		except:
			self._ilabs_cookies = self.cookies_jar()
		
		return self._ilabs_cookies
		
	def cookies_jar(self):
		return Cookies(self, max_age=180)
	
	def flash(self, value = None):
		c = self.cookies()
		if value is not None:
			c['ILFlash'] = str(value)
		else:
			try:
				return c['ILFlash']
			except:
				return None
		
	def get(self, *args):
		if (self.request.accept.best_match(['text/html', 'application/json', 'application/javascript', 'text/json']) != 'text/html'):
			j = self.json(*args)
			if j is not None:
				j = json.dumps(j)
				
				# Check for JSONP
				if self.request.get('callback') != '':
					self.response.headers['Content-Type'] = 'application/javascript'
					j = self.request.get('callback') + '(' + j + ')'
				else:
					self.response.headers['Content-Type'] = 'application/json'
					
				self.response.out.write(j)
				return
		
		template_values = self.perform(*args)
		logging.debug("Using values: %s" % (str(template_values),))
		if template_values is not None:
			path = os.path.join(self.templates_directory(), self.template_name())
			self.response.out.write(template.render(path, template_values))
		
		c = self.cookies()
		del c['ILFlash']
	
	def not_found(self, template_values = {}):
		self.error(404)
		path = os.path.join(self.templates_directory(), self.not_found_template_name())
		self.response.out.write(template.render(path, template_values))
	
	def perform(self, *args):
		return {}
		
	def templates_directory(self):
		return os.path.join(APPLICATION_ROOT_DIRECTORY, 'templates')
		
	def template_name(self):
		return "%s.html" % (self.__class__.__name__,)
		
	def not_found_template_name(self):
		return "404.html"
	
	def json(self, *args):
		return None
