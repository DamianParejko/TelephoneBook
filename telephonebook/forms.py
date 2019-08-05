from django import forms

from .models import Person, Info

class InfoForm(forms.ModelForm):
	class Meta:
		model = Info
		fields = '__all__'

class PersonForm(forms.ModelForm):

	class Meta:
		model = Person
		exclude = '__all__'