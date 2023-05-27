from django.db.models import Model as MyModel
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.timezone import now
from django.db.models import Q

from .utils import *
from .managers import *


# Create your models here.
class Model(MyModel):
	objects = models.Manager()

	class Meta:
		abstract = True


class CustomUser(AbstractUser, PermissionsMixin):
	role = models.CharField(max_length=50, choices=user_roles, default='user')
	avatar = models.ImageField(verbose_name='Аватар', upload_to=get_avatar_path, default=get_default_avatar)
	balance = models.FloatField(verbose_name='Баланс', default=0)


class Sale(Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
	percent = models.IntegerField(verbose_name='Скидка в процентах', blank=True, validators=[
		MaxValueValidator(100),
		MinValueValidator(1)
	])
	description = models.CharField(verbose_name='Описание', max_length=500, blank=True)
	end_of = models.DateField(verbose_name='Действует до', default=get_sale_end_date)

	objects = SaleManager()

	def __str__(self):
		return f'Скидка {self.percent}% для пользователя <{self.user.username}>'

	class Meta:
		verbose_name = 'Скидка'
		verbose_name_plural = 'Скидки'


class OrderStatus(Model):
	text = models.CharField(verbose_name='Статус', max_length=50)

	def __str__(self):
		return self.text

	class Meta:
		verbose_name = 'Статус задачи'
		verbose_name_plural = 'Статусы задач'


class Order(Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, default=None)
	title = models.CharField(verbose_name='Тема заказа', max_length=255, blank=True)
	description = models.TextField(verbose_name='Описание заказа', blank=True)
	price = models.FloatField(verbose_name='Стоимость', blank=True, null=True)
	status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, null=False, default=0)
	created_at = models.DateField(verbose_name='Дата подачи', auto_now=True)
	need_server_setup = models.BooleanField(verbose_name='Требуется установка/настройка сервера', default=False)
	need_bot_setup = models.BooleanField(verbose_name='Требуется установка бота на сервер', default=False)
	need_payment_system = models.BooleanField(verbose_name='Требуется платёжная система', default=False)
	email = models.EmailField(verbose_name='Email для чека', default=None, null=True)
	tz_file = models.FileField(verbose_name='Файл с техническим заданием', upload_to=get_order_tz_path, default=None, null=True, blank=True)

	def get_price(self):
		return {
			'Разработка бота': 3000,
			'Настройка сервера': int(self.need_server_setup) * 500,
			'Установка бота': int(self.need_bot_setup) * 500,
			'Подключение платёжной системы': int(self.need_payment_system) * 1500
		}

	def set_price(self):
		self.price = int(self.need_server_setup) * 500 + int(self.need_bot_setup) * 500 + int(self.need_payment_system) * 1500 + 3000
		self.save()

	def __str__(self):
		return f'Заказ №{self.id} {self.user.username} ({self.status.text})'

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'


class DefaultProfileImage(Model):
	photo = models.ImageField(verbose_name='Изображение', upload_to='default_profile_images')


class PaymentHistory(Model):
	manager = models.ForeignKey(get_user_model(), verbose_name='Кто выдал', on_delete=models.SET_NULL, null=True, related_name='payment_history_manager')
	to = models.ForeignKey(get_user_model(), verbose_name='Кому выдал', on_delete=models.SET_NULL, null=True, related_name='payment_history_to')
	amount = models.FloatField(verbose_name='Количество бонусов', default=0)
	date = models.DateField(verbose_name='Дата', auto_now_add=True)

	def __str__(self):
		return f'Выдача бонусов от {self.manager.username} для {self.to.username}'

	class Meta:
		verbose_name = 'Чек на выдачу бонусов'
		verbose_name_plural = 'Истории выдачи бонусов'


class Message(Model):
	user = models.ForeignKey(get_user_model(), verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
	text = models.CharField(verbose_name='Текст сообщения', max_length=500, default='')

	class Meta:
		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'
