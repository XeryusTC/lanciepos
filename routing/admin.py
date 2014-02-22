from django.contrib import admin
from routing.models import Client

class ClientAdmin(admin.ModelAdmin):
	fieldsets = [(None, {'fields': ['user', 'ipaddress']}),
		('Signing status', {'fields': ['rule_signed', 'access_granted']}),
	]
	list_display = ('__str__', 'rule_signed', 'access_granted')
	search_fields = ['question']
	list_filter = ['rule_signed', 'access_granted']

admin.site.register(Client, ClientAdmin)
