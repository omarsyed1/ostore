from django import forms

from django.contrib.auth.models import User
from models import *

import re

class AccountNameForm(forms.Form):
	new_account_name = forms.CharField(max_length = 40)

	def clean(self):
		cleaned_data = super(AccountNameForm, self).clean()
		regex = re.compile("^\w+")
		if not regex.match(cleaned_data.get('new_account_name')):
			raise forms.ValidationError("Account name can only contain numbers and letters")
		return cleaned_data

class RegistrationForm(forms.Form):
  email = forms.CharField(max_length = 40)
  first_name = forms.CharField(max_length = 20)
  last_name = forms.CharField(max_length = 20)
  password1 = forms.CharField(max_length = 50, 
                              label='Password', 
                              widget = forms.PasswordInput())
  password2 = forms.CharField(max_length = 50, 
                              label='Confirm password',  
                              widget = forms.PasswordInput())
   


  # Customizes form validation for properties that apply to more
  # than one field.  Overrides the forms.Form.clean function.
  def clean(self):
      # Calls our parent (forms.Form) .clean function, gets a dictionary
      # of cleaned data as a result
      cleaned_data = super(RegistrationForm, self).clean()

      # Confirms that the two password fields match
      password1 = cleaned_data.get('password1')
      password2 = cleaned_data.get('password2')
      if password1 and password2 and password1 != password2:
          raise forms.ValidationError("Passwords did not match.")

      # We must return the cleaned data we got from our parent.
      return cleaned_data


  # Customizes form validation for the username field.
  def clean_username(self):
      # Confirms that the username is not already present in the
      # User model database.
      email = self.cleaned_data.get('email')
      if User.objects.filter(username__exact=email):
          raise forms.ValidationError("Email is already taken.")

      # We must return the cleaned data we got from the cleaned_data
      # dictionary
      return email