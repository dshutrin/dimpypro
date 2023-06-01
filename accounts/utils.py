import datetime
from random import choice as ch
from django.conf.global_settings import MEDIA_URL, MEDIA_ROOT
from django.conf import settings
import os
import datetime
from datetime import date, timedelta


user_roles = (
	('user', 'user'),
	('manager', 'manager'),
	('admin', 'admin'),
)


def get_avatar_path(user_obj, filename):
	return f'avatars/{user_obj.id}/{filename}'


def get_default_avatar():
	return ch((
		os.path.join(MEDIA_URL, 'default_profile_images', 'default_avatar_1.png'),
		os.path.join(MEDIA_URL, 'default_profile_images', 'default_avatar_2.png'),
		os.path.join(MEDIA_URL, 'default_profile_images', 'default_avatar_3.png')
	))


def get_sale_end_date():
	return datetime.date.today() + datetime.timedelta(days=3)


def get_order_tz_path(order_obj, filename, full=False):
	path = f'specifications/{order_obj.user.username}/{filename}'
	if not full:
		return f'specifications/{order_obj.user.username}/{filename}'
	while os.path.exists(os.path.join(settings.BASE_DIR, 'media', path)):
		filename = f'1{filename}'
		path = f'specifications/{order_obj.user.username}/{filename}'
	full_path = os.path.join(settings.BASE_DIR, 'media', path)

	return full_path, path


def get_util_file_path(util_obj, filename):
	return f'utils/{filename}'


def get_util_instruction_path(util_obj, filename):
	return f'utils/{filename}'
