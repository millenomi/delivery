import plistlib

class ProvisioningProfile:
	def __init__(self, file = None, content = None):
		bytestring = content
		if not bytestring:
			bytestring = file.read()
			
		start = bytestring.index("<?xml")
		end = bytestring.index("</plist>")
		end += len("</plist>")
		self.info = plistlib.readPlistFromString(bytestring[start:end])
		
		try:
			self.name = self.info['Name']
		except:
			self.name = None
			
		try:
			self.uuid = self.info['UUID']
		except:
			self.uuid = None
		
		try:
			self.devices = self.info['ProvisionedDevices']
		except:
			self.devices = None
			
		try:
			self.expiration = self.info['ExpirationDate']
		except:
			self.expiration = None
		
		try:
			self.entitlements = self.info['Entitlements']
		except:
			self.entitlements = None
		
		self.development = False
		try:
			self.development = (self.entitlements['get-task-allow'] == True)
		except:
			pass
			