from django import forms
from django.contrib.auth.models import User

class RequestAccessForm(forms.Form):
	email = forms.EmailField(error_messages = {'non_existent': 'You have to use the email address that you\'ve signed up with'})

	def clean_email(self):
		try:
			User.objects.get(email=self.cleaned_data['email'])
		except User.DoesNotExist:
			raise forms.ValidationError(self.fields['email'].error_messages['non_existent'])
			
		return self.cleaned_data['email']
