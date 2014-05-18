from django.contrib import admin

from pointofsale.models import *

class DrinkAdmin(admin.ModelAdmin):
	fields = ['name', 'price']
	list_display = ('name', 'price', 'get_times_bought')


class FoodAdmin(admin.ModelAdmin):
	fields = ('name', 'price', 'description')
	list_display = ('name', 'price')


class DinnerAdmin(admin.ModelAdmin):
	fields = ('food', 'day', 'deadline')
	list_display = ('food', 'day', 'deadline', 'get_times_bought', 'is_still_available')
	list_filter = ('day',)


class AccountAdmin(admin.ModelAdmin):
	readonly_fields = ('get_spend_on_drinks', 'get_spend_on_dinner', 'get_credits_used', 'get_credits_left', 'get_drinks_bought', 'get_dinners_bought')
	fieldsets = (
		(None, {
			'fields': ('user', 'credits', 'qr_code')
		}),
		('Registration information', {
			'fields': ('address', 'city', 'iban'),
		}),
		('Statistics', {
			'classes': ('collapse',),
			'fields': ('get_drinks_bought', 'get_dinners_bought', 'get_credits_used', 'get_credits_left', 'get_spend_on_drinks', 'get_spend_on_dinner')
		}),
	)
	list_display = ('__str__', 'credits', 'get_credits_used', 'qr_code', 'address', 'city', 'iban')

class DrinkOrderAdmin(admin.ModelAdmin):
	list_display = ('time', 'drink', 'account')
	readonly_fields = ('time',)
	list_filter = ('drink', 'account')

class DinnerOrderAdmin(admin.ModelAdmin):
	list_display = ('time', 'dinner', 'account')
	readonly_fields = ('time',)
	list_filter = ('dinner', 'account')

admin.site.register(Drink, DrinkAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Dinner, DinnerAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(DrinkOrder, DrinkOrderAdmin)
admin.site.register(DinnerOrder, DinnerOrderAdmin)
