from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Drink(models.Model):
	name = models.CharField(max_length=32)
	price = models.SmallIntegerField()
	
	def get_times_bought(self):
		return self.drinkorder_set.count()
	get_times_bought.short_description = 'Times bought'
	
	def __str__(self):
		return self.name


class Food(models.Model):
	name = models.CharField(max_length=32)
	description = models.TextField()
	price = models.SmallIntegerField()
	
	class Meta:
		verbose_name_plural = 'food'
	
	def __str__(self):
		return self.name


class Dinner(models.Model):
	MONDAY    = 'MON'
	TUESDAY   = 'TUE'
	WEDNESDAY = 'WED'
	THURSDAY  = 'THU'
	FRIDAY    = 'FRI'
	SATURDAY  = 'SAT'
	SUNDAY    = 'SUN'
	DAY_CHOICES = ((MONDAY, 'Monday'),
		(TUESDAY,   'Tuesday'),
		(WEDNESDAY, 'Wednesday'),
		(THURSDAY,  'Thursday'),
		(FRIDAY,    'Friday'),
		(SATURDAY,  'Saturday'),
		(SUNDAY,    'Sunday'))
	
	day = models.CharField(max_length=3, choices=DAY_CHOICES, default=FRIDAY)
	food = models.ForeignKey(Food)
	deadline = models.DateTimeField()
	
	class Meta:
		unique_together = ("food", "day")
	
	def get_times_bought(self):
		return self.dinnerorder_set.count()
	get_times_bought.short_description = 'Times bought'
	
	def is_still_available(self):
		return self.deadline >= timezone.now()
	is_still_available.admin_order_field = 'deadline'
	is_still_available.boolean = True
	
	def __str__(self):
		return "{} ({})".format(self.food.name, self.get_day_display())


class Account(models.Model):
	user = models.OneToOneField(User)
	
	credits = models.IntegerField(default=0)
	qr_code = models.CharField(max_length=16, blank=True)
	qr_code.verbose_name = 'QR code'
	#rules_signed = models.BooleanField(default=False)
	
	# allow buying stuff
	drinks_bought = models.ManyToManyField(Drink, through='DrinkOrder')
	dinners_bought = models.ManyToManyField(Dinner, through='DinnerOrder')
	
	def get_drinks_bought(self):
		return self.drinkorder_set.count()
	get_drinks_bought.short_description = 'Total drinks bought'
	
	def get_dinners_bought(self):
		return self.dinnerorder_set.count()
	get_dinners_bought.short_description = 'Total dinners bought'
	
	def get_spend_on_drinks(self):
		drink = self.drinkorder_set.all().aggregate(drink_used=models.Sum('drink__price'))
		if drink['drink_used'] is None:
			return 0
		return int(drink['drink_used'])
	get_spend_on_drinks.short_description = 'Credit used for drinks'
	
	def get_spend_on_dinner(self):
		dinner = self.dinnerorder_set.all().aggregate(dinner_used=models.Sum('dinner__food__price'))
		if dinner['dinner_used'] is None:
			return 0
		return int(dinner['dinner_used'])		
	get_spend_on_dinner.short_description = 'Credit used for dinner'
	
	def get_credits_used(self):
		return self.get_spend_on_drinks() + self.get_spend_on_dinner()
	get_credits_used.short_description = 'Credits used'
	
	def get_credits_left(self):
		return self.credits - self.get_credits_used()
	get_credits_left.short_description = 'Credits left'
	
	def __str__(self):
		return self.user.get_full_name()


class DrinkOrder(models.Model):
	account = models.ForeignKey(Account)
	drink = models.ForeignKey(Drink)
	time = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ["-time"]
		get_latest_by = "time"
	
	def __str__(self):
		return "[{1}]  {2} - {0}".format(self.account, self.time, self.drink)


class DinnerOrder(models.Model):
	account = models.ForeignKey(Account)
	dinner = models.ForeignKey(Dinner)
	time = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ["-time"]
		get_latest_by = "time"
	
	def __str__(self):
		return "[{1}] {2} -{0}".format(self.account.user.get_full_name(), self.time, self.dinner)

