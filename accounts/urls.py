from django.urls import path, register_converter
from .views import *
from .converters import FloatUrlParameterConverter

register_converter(FloatUrlParameterConverter, 'float')

urlpatterns = [
	path('', self_page),
	path('get_balance', get_user_balance),
	path('order/create', create_order),
	path('orders', all_orders),
	path('orders/<int:order_id>', order_detail),
	path('orders/<int:order_id>/edit', edit_order),
	path('order/get_price/<str:need_server_setup>/<str:need_bot_setup>/<str:need_payment_system>', get_order_price),
	path('admin', admin),
	path('admin/bonuses', bonuses),
	path('admin/orders', admin_orders),
	path('admin/order/<int:order_id>', admin_order),
	path('admin/order/<int:order_id>/send_msg', order_messages),
	path('admin/order/<int:order_id>/set_git_link', set_git_link),
	path('admin/order/<int:order_id>/get_git_link', get_git_link),
	path('admin/order/<int:order_id>/set_status/<int:status_id>', set_order_status),
	path('admin/get_last_week_orders', get_last_week_orders_view),
	path('admin/bonuses/<int:user_id>', bonus_page),
	path('admin/bonuses/get_users/<str:data>', get_users),
	path('admin/bonuses/new/<int:user_id>/<float:bonus_count>', get_bonus),
	path('admin/bonus_history', bonus_history),
	path('utils', utils),
	path('utils/<int:util_id>', util_detail)
]

