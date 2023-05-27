from django.urls import path, register_converter
from .views import *
from .converters import FloatUrlParameterConverter

register_converter(FloatUrlParameterConverter, 'float')

urlpatterns = [
	path('', self_page),
	path('order/create', create_order),
	path('orders', all_orders),
	path('orders/<int:order_id>', order_detail),
	path('order/get_price', get_order_price),
	path('admin', admin),
	path('admin/bonuses', bonuses),
	path('admin/orders', admin_orders),
	path('admin/order/<int:order_id>', admin_order),
	path('admin/order/<int:order_id>/send_msg', order_messages),
	path('admin/bonuses/<int:user_id>', bonus_page),
	path('admin/bonuses/get_users/<str:data>', get_users),
	path('admin/bonuses/new/<int:user_id>/<float:bonus_count>', get_bonus),
	path('admin/bonus_history', bonus_history)
]
