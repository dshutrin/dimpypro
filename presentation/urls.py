from django.urls import path
from .views import *


urlpatterns = [
	path('', home),
	path('login', login_view),
	path('logout', logout_view),
	path('register', register_view)
]
