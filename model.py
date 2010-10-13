from google.appengine.ext.db import *
from google.appengine.ext import blobstore

# The profile's UUID is the key_name
class com_apple_iOS_ProvisioningProfile(Model):
	name = StringProperty()
	devices = StringListProperty()
	data = BlobProperty()
	