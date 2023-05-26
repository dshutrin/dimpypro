import datetime
from random import choice as ch
from django.conf.global_settings import MEDIA_URL
import os
import datetime


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
