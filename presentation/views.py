from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *


# Create your views here.
def home(request):
	return render(request, 'presentation/home.html')


def login_view(request):
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/account')
		else:
			return render(request, 'presentation/login_page.html', {'form': LoginForm()})
	elif request.method == 'GET':
		return render(request, 'presentation/login_page.html', {'form': LoginForm()})


def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()
			login(request, user)
			return HttpResponseRedirect('/account')
		else:
			return render(request, 'presentation/register_page.html', {'form': form})
	elif request.method == 'GET':
		return render(request, 'presentation/register_page.html', {'form': RegisterForm()})


@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
