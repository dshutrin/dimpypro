import datetime
from django.db.models import Manager


class SaleManager(Manager):
	def get_queryset(self, *args, **kwargs):
		super().get_queryset(*args, **kwargs).filter(end_of__lt=datetime.date.today()).delete()
		return super().get_queryset(*args, **kwargs).all()
