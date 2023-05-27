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


class OrderForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
			visible.field.widget.attrs['placeholder'] = visible.field.label
			visible.field.widget.attrs['oninput'] = "get_order_price()"

		self.fields['description'].widget.attrs['style'] = 'min-height: 200px;'
		self.fields['need_server_setup'].widget.attrs['class'] = 'form-check-input'
		self.fields['need_payment_system'].widget.attrs['class'] = 'form-check-input'
		self.fields['need_bot_setup'].widget.attrs['class'] = 'form-check-input'

	class Meta:
		model = Order
		fields = (
			'title', 'description', 'need_server_setup', 'need_bot_setup', 'need_payment_system', 'tz_file', 'email'
		)

	def title(self):
		return self.fields['title']

	def description(self):
		return self.fields['description']

	def need_server_setup(self):
		return self.fields['need_server_setup']

	def need_bot_setup(self):
		return self.fields['need_bot_setup']

	def tz_file(self):
		return self.fields['tz_file']

	def need_payment_system(self):
		return self.fields['need_payment_system']

	def email(self):
		return self.fields['promo']
