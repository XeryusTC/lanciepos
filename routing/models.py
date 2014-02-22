from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
	user = models.OneToOneField(User)
	ipaddress = models.IPAddressField()
	rule_signed = models.BooleanField(default=False)
	access_granted = models.BooleanField(default=False)
	
	def __str__(self):
		return "{}: {}".format(self.user.get_full_name(), self.ipaddress)

