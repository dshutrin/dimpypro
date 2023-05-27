clear_components_box = () => {
	document.getElementById('components_box').replaceChildren()
}

create_element = (name, amount) => {
	li = document.createElement('li')
	li.className = 'list-group-item d-flex justify-content-between lh-sm'
	div = document.createElement('div')
	h6 = document.createElement('h6')
	h6.className = 'my-0'
	h6.innerHTML = name
	div.appendChild(h6)
	li.appendChild(div)
	span = document.createElement('span')
	span.className = 'text-body-secondary'
	span.innerHTML = amount
	li.appendChild(span)
	return li
}

create_total_sum = (amount) => {
	li = document.createElement('li')
	li.className = 'list-group-item d-flex justify-content-between lh-sm'
	div = document.createElement('div')
	h6 = document.createElement('h6')
	h6.className = 'my-0'
	h6.innerHTML = 'Всего'
	div.appendChild(h6)
	li.appendChild(div)
	span = document.createElement('span')
	span.className = 'text-body-secondary fw-bold'
	span.innerHTML = amount
	li.appendChild(span)
	return li
}

fill_components_box = (data) => {
	clear_components_box()
	box_ul = document.getElementById('components_box')

	let total_amount = 0

	for (const [key, value] of Object.entries(data)) {
		total_amount += value
		box_ul.appendChild(
			create_element(key, value)
		)
	}

	box_ul.appendChild(create_total_sum(total_amount))
}

get_order_price = () => {
	let xhr = new XMLHttpRequest();
	xhr.open('POST', '/account/order/get_price');
	xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val())

	let need_server_setup = document.getElementById("id_need_server_setup").checked
	let need_bot_setup = document.getElementById("id_need_bot_setup").checked
	let need_payment_system = document.getElementById("id_need_payment_system").checked
	let promo = $('#id_promo').val()

	let data = new FormData();
	data.append('need_server_setup', need_server_setup);
	data.append('need_bot_setup', need_bot_setup);
	data.append('need_payment_system', need_payment_system);
	data.append('promo', promo);

	xhr.send(data)
	xhr.responseType = 'json'

	xhr.onloadend = () => {
		fill_components_box(xhr.response)
	}
}

get_order_price()
