from django import forms
from django.contrib.auth import get_user_model

from .models import *


class SearchUserForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control text-center'
			visible.field.widget.attrs['placeholder'] = 'Поиск пользователя'
			visible.field.widget.attrs['oninput'] = 'search_users()'

	data = forms.CharField(label='Поиск пользователя', max_length=255)


class BonusForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control text-center'
		self.fields['bonus_count'].widget.attrs['placeholder'] = self.fields['bonus_count'].label

	bonus_count = forms.FloatField(min_value=0.1, label='Бонусы')


class AvatarForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = get_user_model()
		fields = ('avatar', )
