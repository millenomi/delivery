import tools as t
import model as m
import logging
import apple_ios as a

from google.appengine.ext import db

def add(list):
	list.append(('/com.apple.ios/provisioning/add', AddProvisioning))
	list.append(('/com.apple.ios/provisioning/(.*)', GetProvisioning))

class AddProvisioning(t.TemplateServingHandler):
	def perform(self):
		return { 'flash': self.flash() }
	
	def post(self):
		blob = self.request.get('profile')
		try:
			profile = a.ProvisioningProfile(content = blob)
		except:
			self.flash('The provisioning profile is invalid.')
			self.redirect('/com.apple.ios/provisioning/add')
			return
		
		if profile.uuid is None:
			self.flash('The provisioning profile does not contain a UUID.')
			self.redirect('/com.apple.ios/provisioning/add')
			return
		
		def tx():
			o = m.com_apple_iOS_ProvisioningProfile.get_by_key_name(profile.uuid)
			if not o:
				o = m.com_apple_iOS_ProvisioningProfile(key_name = profile.uuid)
			o.name = profile.name
			o.data = blob
			o.devices = profile.devices
			o.put()
			
		db.run_in_transaction(tx)
		
		self.redirect('/com.apple.ios/provisioning/add')
		
class GetProvisioning(t.TemplateServingHandler):
	def get(self, uuid):
		logging.debug(uuid)
		o = m.com_apple_iOS_ProvisioningProfile.get_by_key_name(uuid)
		if o is None:
			return self.not_found()
		
		self.response.headers['Content-Disposition'] = ("attachment; filename=%s.mobileprovision" % (uuid,))
		self.response.headers['Content-Type'] = 'application/octet-stream'
		self.response.out.write(o.data)
	