show_toast = () => {
	var toastElList = [].slice.call(document.querySelectorAll('.toast'))
	var toastList = toastElList.map(function(toastEl) {
		return new bootstrap.Toast(toastEl)
	});
	toastList.forEach(toast => toast.show());
};

document.getElementById("compleat_button").onclick = () => {
	let xhr = new XMLHttpRequest()

	let user_id = document.getElementById('user_id').value
	let bonus_count = document.getElementById('id_bonus_count').value

	if (bonus_count.indexOf('.') > -1){} else {
		bonus_count += '.0'
	}

	let header = document.getElementById('toast_header')
	let body = document.getElementById('payment_success_text')
	let header_div = document.getElementById('header_div')

	xhr.open('POST', '/account/admin/bonuses/new/' + user_id + '/' + bonus_count)
	let csrftoken = $("[name=csrfmiddlewaretoken]").val();
	xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.send()
    xhr.responseType = 'json'

	xhr.onloadend = () => {
		if (xhr.status == 404) {
			header.innerHTML = 'Ошибка пополнения!'
			body.innerHTML = 'Не удалось провести операцию!'
			header_div.classList.remove('text-bg-success')
			header_div.classList.remove('text-bg-danger')
			header_div.classList.add('text-bg-danger')
			console.clear()
			show_toast()
		} else {
			if (xhr.response['ok'] == true){
				header.innerHTML = 'Успешное пополнение!'
				header_div.classList.remove('text-bg-danger')
				header_div.classList.remove('text-bg-success')
				header_div.classList.add('text-bg-success')
				document.getElementById('bonus_form').reset()
			} else {
				header.innerHTML = 'Ошибка пополнения!'
				header_div.classList.remove('text-bg-success')
				header_div.classList.remove('text-bg-danger')
				header_div.classList.add('text-bg-danger')
			}
			body.innerHTML = xhr.response['message']
			show_toast()
		}
	}
}
