from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.db.models import Q

from .models import *
from .forms import *


# Create your views here.
@login_required
def self_page(request):
	sales = Sale.objects.filter(user=request.user).order_by('-percent')
	if sales.count() > 5:
		sales = sales[:5]

	orders = Order.objects.filter(user=request.user).order_by('-status__id')
	if orders.count() > 4:
		orders = orders[:4]

	return render(request, 'accounts/profile.html', {
		'sales': sales,
		'sales_count': sales.count(),
		'orders': orders,
		'orders_count': orders.count()
	})


@login_required
def admin(request):
	if request.user.is_superuser:
		return render(request, 'accounts/admin_panel.html', {
			'total_users_count': get_user_model().objects.all().count
		})
	else:
		return HttpResponseRedirect('/')


@login_required
def bonuses(request):
	if request.user.is_superuser:
		if request.method == 'GET':
			return render(request, 'accounts/bonuses.html', {'form': SearchUserForm(), 'users': [{
					'username': x.username,
					'id': x.id
				} for x in get_user_model().objects.all()]})
		else:
			return HttpResponse(f'HTTP method {request.method} not allowed on this page!')
	else:
		return HttpResponseRedirect('/')


@login_required
def get_users(request, data):
	if request.user.is_superuser:
		if request.method == 'POST':
			users = []
			if data == 'ALL_USERS':
				users = [{
					'username': x.username,
					'id': x.id,
					'first_name': x.first_name,
					'last_name': x.last_name
				} for x in get_user_model().objects.all()]
			else:
				users = [{
					'username': x.username,
					'id': x.id,
					'first_name': x.first_name,
					'last_name': x.last_name
				} for x in get_user_model().objects.filter(username__contains=data)]
			print(users)
			return JsonResponse({'count': len(users), 'objects': users})
		else:
			return HttpResponse(f'HTTP method {request.method} not allowed on this page!')
	else:
		return HttpResponseRedirect('/')


@login_required
def all_orders(request):
	orders_ = Order.objects.filter(user__id=request.user.id)
	return render(request, 'accounts/orders_page.html', {
		'orders_count': len(orders_),
		'statuses': [x.text for x in OrderStatus.objects.all() if x in [s.status for s in orders_]][::-1],
		'orders': orders_
	})


@login_required
def order_detail(request, order_id):

	order = Order.objects.get(id=order_id)
	buttons = [0, 0, 0, 0, 0, 0]
	for i in range(1, order.status.id+1):
		buttons[i-1] = 1

	oft = 'None'
	if order.tz_file:
		if order.tz_file.path.endswith('docx'):
			oft = 'docx'
		else:
			oft = 'pdf'

	messages = Message.objects.filter(order__id=order_id)

	return render(request, 'accounts/order_detail.html', {
		'stat1': buttons[0],
		'stat2': buttons[1],
		'stat3': buttons[2],
		'stat4': buttons[3],
		'stat5': buttons[4],
		'stat6': buttons[5],
		'percent': (sum(buttons)-1) * 20,
		'order': order,
		'messages': messages,
		'messages_count': messages.count,
		'order_file_type': oft
	})


@login_required
def bonus_page(request, user_id):
	if request.user.is_superuser:
		user = get_user_model().objects.filter(id=user_id)

		if request.method == 'POST':
			form = BonusForm(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				user = get_user_model().objects.get(id=user_id)
				user.balance += data['bonus_count']
				user.save()
				return HttpResponseRedirect('/account/admin/bonuses')
			else:
				return render(request, 'accounts/bonus_page.html', {'form': form})

		if len(user) > 0:
			return render(request, 'accounts/bonus_page.html', {'form': BonusForm(initial={'user': user_id}), 'user': user[0]})
		else:
			return HttpResponse('User not found!')
	else:
		return HttpResponse('Not found!')


@login_required
def get_bonus(request, user_id, bonus_count):
	user = [x for x in get_user_model().objects.filter(id=user_id)]
	if len(user) > 0:
		user[0].balance += bonus_count
		user[0].save()

		PaymentHistory(
			manager=request.user,
			to=user[0],
			amount=bonus_count
		).save()

		for hist in PaymentHistory.objects.all():
			print(hist.date)

		return JsonResponse({'ok': True, 'message': f'Баланс пользователя {user[0].username} пополнен на {bonus_count}!'})
	return JsonResponse({'ok': False, 'message': f'Не удалось пополнить баланс пользователя {user[0].username}!'})


@login_required
def admin_orders(request):
	if request.user.is_superuser:
		orders_ = Order.objects.all().order_by('-created_at')

		return render(request, 'accounts/admin_orders_page.html', {
			'orders': orders_,
			'statuses': [x.text for x in OrderStatus.objects.all() if len([a for a in orders_ if a.status == x]) > 0]
		})

	else:
		return HttpResponseRedirect('/')


@login_required
def admin_order(request, order_id):
	if request.user.is_superuser:

		order = Order.objects.filter(id=order_id)
		if len(order) > 0:

			order = order[0]

			buttons = [0, 0, 0, 0, 0, 0]
			for i in range(1, order.status.id + 1):
				buttons[i - 1] = 1

			messages = Message.objects.filter(order=order)
			oft = 'None'
			if order.tz_file:
				if order.tz_file.path.endswith('docx'):
					oft = 'docx'
				else:
					oft = 'pdf'

			return render(request, 'accounts/admin_order_detail.html', {
				'order': order,
				'order_status': order.status.text,
				'percent': (sum(buttons) - 1) * 20,
				'messages': messages,
				'messages_count': messages.count,
				'order_file_type': oft,
				'statuses': OrderStatus.objects.all()
			})

		else:
			return HttpResponse('Order not found!')

	else:
		return HttpResponseRedirect('/')


@login_required
def bonus_history(request):
	history = PaymentHistory.objects.all().order_by('-date')[:25]
	orders = Order.objects.all()
	orders_history = orders.order_by('-created_at')[:25]

	utils_top_ = {}
	for act in PaidUtils.objects.all():
		if act.util.title in utils_top_:
			utils_top_[act.util] += 1
		else:
			utils_top_.update({act.util: 1})

	utils_top = []
	for act in utils_top_:
		utils_top.append((act, utils_top_[act]))

	utils_top = sorted(utils_top)

	class Top:
		def __init__(self, util, count):
			self.util = util.title
			self.count = count
			self.price = util.price
			self.total_amount = count * util.price

	utils_top = [Top(x[0], x[1]) for x in utils_top]

	return render(request, 'accounts/admin_history.html', {
		'payments': history,
		'utils_top': utils_top,
		'summ': sum([x.amount for x in history]),
		'not_realized': sum([x.price for x in orders.filter(~Q(status__text='Готово'))]),
		'realized': sum([x.price for x in orders.filter(status__text='Готово')]),
		'paid_utils': sum([x.util.price for x in PaidUtils.objects.all()]),
		'total_realized_price': sum([x.price for x in orders]) + sum([x.util.price for x in PaidUtils.objects.all()]),
		'total_payments_price': sum([x.amount for x in PaymentHistory.objects.all()]),
		'orders': orders_history
	})


@login_required
def order_messages(request, order_id):
	if request.method == 'POST':

		message = Message.objects.create(
			user=request.user,
			order=Order.objects.get(id=order_id),
			text=request.body.decode('utf-8')
		)
		message.save()

		return JsonResponse({
			'ok': True,
			'message_text': message.text,
			'user': message.user.username,
			'avatar': message.user.avatar.url
		})
	else:
		return JsonResponse({'ok': False})


@login_required
def create_order(request):
	form = OrderForm()
	payment_status = 'True'

	if request.POST:
		form = OrderForm(request.POST)

		post = [
			request.POST.get(x, False) for x in ['title', 'description', 'email']
		]
		if all(post):
			if 'tz_file' in request.FILES:
				order = Order.objects.create(
					user=request.user,
					title=request.POST['title'] or 'False',
					description=request.POST['description'] or '',
					status=OrderStatus.objects.get(id=1),
					need_server_setup={'on': True, 'off': False}[request.POST['need_server_setup']] if ('need_server_setup' in request.POST) else False,
					need_bot_setup={'on': True, 'off': False}[request.POST['need_bot_setup']] if ('need_bot_setup' in request.POST) else False,
					need_payment_system={'on': True, 'off': False}[request.POST['need_payment_system']] if ('need_payment_system' in request.POST) else False,
					email=request.POST['email'],
					tz_file=request.FILES['tz_file']
				)
			else:
				order = Order.objects.create(
					user=request.user,
					title=request.POST['title'] or 'False',
					description=request.POST['description'] or '',
					status=OrderStatus.objects.get(id=1),
					need_server_setup={'on': True, 'off': False}[request.POST['need_server_setup']] if ('need_server_setup' in request.POST) else False,
					need_bot_setup={'on': True, 'off': False}[request.POST['need_bot_setup']] if ('need_bot_setup' in request.POST) else False,
					need_payment_system={'on': True, 'off': False}[request.POST['need_payment_system']] if ('need_payment_system' in request.POST) else False,
					email=request.POST['email']
				)

			order.set_price()
			return HttpResponseRedirect('/account/orders')

	return render(request, 'accounts/create_order_page.html', {'form': form})


@login_required
def get_order_price(request, need_server_setup, need_bot_setup, need_payment_system):
	if request.method == 'GET':
		order = Order(
			need_server_setup={'true': True, 'false': False}[need_server_setup],
			need_bot_setup={'true': True, 'false': False}[need_bot_setup],
			need_payment_system={'true': True, 'false': False}[need_payment_system]
		)
		return JsonResponse(order.get_price())
	else:
		return JsonResponse({'error': True})


@login_required
def get_user_balance(request):
	return JsonResponse({'balance': request.user.balance})


@login_required
def set_git_link(request, order_id):
	if request.method == 'POST':
		if request.user.is_superuser:
			order = Order.objects.get(id=order_id)

			print(request.body)
			new_link = request.body.decode('utf-8')

			order.answer_link = new_link
			order.save()
			return JsonResponse({'ok': True})
		else:
			return JsonResponse({'ok': False})
	else:
		return JsonResponse({'ok': False})


@login_required
def get_git_link(request, order_id):
	order = Order.objects.filter(id=order_id)
	if len(order) > 0:
		order = order[0]
		return JsonResponse({'ok': True, 'git_link': order.answer_link})
	else:
		return JsonResponse({'ok': False})


@login_required
def get_last_week_orders_view(request):
	if request.user.is_superuser:
		today = date.today()
		seven_day_before = today - timedelta(days=7)
		last_week_orders = Order.objects.filter(created_at__gte=seven_day_before)
		ans = {'ok': True, 'labels': [
			str(today - timedelta(days=i)) for i in reversed(range(7))
		], 'values': [0, 0, 0, 0, 0, 0, 0]}

		for order in last_week_orders:
			ans['values'][
				ans['labels'].index(str(order.created_at))
			] += 1

		statuses = {}
		for order in Order.objects.all():
			if not order.status.text in statuses:
				statuses.update({order.status.text: 1})
			else:
				statuses[order.status.text] += 1

		ans.update({'statuses': statuses})

		return JsonResponse(ans)
	else:
		return JsonResponse({'error': True})


@login_required
def set_order_status(request, order_id, status_id):
	order = Order.objects.filter(id=order_id)
	status = OrderStatus.objects.filter(id=status_id)
	if len(order) and len(status):
		order[0].status = status[0]
		order[0].save()
		return JsonResponse({'ok': True, 'status': status[0].text})
	else:
		return JsonResponse({'ok': False})


@login_required
def edit_order(request, order_id):
	form = OrderForm()
	payment_status = 'True'
	order = Order.objects.get(id=order_id)

	if request.POST:
		form = OrderForm(request.POST)

		post = [
			request.POST.get(x, False) for x in ['title', 'description', 'email']
		]
		if all(post):

			order.title = request.POST['title'] or 'False'
			order.description = request.POST['description'] or ''
			order.status = OrderStatus.objects.get(id=1)
			order.need_server_setup = {'on': True, 'off': False}[request.POST['need_server_setup']] if ('need_server_setup' in request.POST) else False
			order.need_bot_setup = {'on': True, 'off': False}[request.POST['need_bot_setup']] if ('need_bot_setup' in request.POST) else False
			order.need_payment_system = {'on': True, 'off': False}[request.POST['need_payment_system']] if ('need_payment_system' in request.POST) else False
			order.email = request.POST['email']

			if request.FILES:
				os.remove(os.path.join(MEDIA_URL, order.tz_file.path))
				order.tz_file = request.FILES['tz_file']

			order.set_price()
			return HttpResponseRedirect('/account/orders')

	else:
		form = OrderForm(initial={
			'user': order.user,
			'title': order.title,
			'description': order.description,
			'status': order.status,
			'need_server_setup': order.need_server_setup,
			'need_bot_setup': order.need_bot_setup,
			'need_payment_system': order.need_payment_system,
			'email': order.email
		})

	if order.tz_file:
		return render(request, 'accounts/create_order_page.html', {'form': form, 'edit': True, "file": True, 'path': order.tz_file.url})
	else:
		return render(request, 'accounts/create_order_page.html', {'form': form, 'edit': True, "file": False})


@login_required
def utils(request):

	class UtilView:
		def __init__(self, util, paid):
			self.util = util
			self.paid = paid

	utils = []
	for util in Utilit.objects.all():
		if len(PaidUtils.objects.filter(user=request.user, util=util)) > 0:
			utils.append(UtilView(util, True))
		else:
			utils.append(UtilView(util, False))

	return render(request, 'accounts/utils_page.html', {'utils': utils})


@login_required
def util_detail(request, util_id):
	util = Utilit.objects.get(id=util_id)
	is_paid = len(PaidUtils.objects.filter(user=request.user, util=util)) > 0
	instr = open(util.instruction.path, 'r', encoding='utf-8')
	instr = instr.read()

	return render(request, 'accounts/util_detail.html', {
		'util': util,
		'instruction': instr,
		'is_paid': is_paid
	})
