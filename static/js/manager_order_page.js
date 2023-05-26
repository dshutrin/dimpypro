show_toast = () => {
	var toastElList = [].slice.call(document.querySelectorAll('.toast'))
	var toastList = toastElList.map(function(toastEl) {
		return new bootstrap.Toast(toastEl)
	});
	toastList.forEach(toast => toast.show());
};

send_manager_message = () => {
	let message = document.getElementById('manager_input').value
	let body = document.getElementById('payment_success_text')

	if (message) {
		document.getElementById('manager_input').value = ''

		let order_id = document.getElementById('order_id_input').value

		let xhr = new XMLHttpRequest()
		xhr.open('POST', '/account/admin/order/' + order_id + '/send_msg', true)
		xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val())
	    xhr.send(message)
	    xhr.responseType = 'json'

	    xhr.onloadend = () => {
	        console.log(xhr.response)
			if (xhr.response['ok'] == false) {
				body.innerHTML = 'Не удалось отправить сообщение!'
				show_toast()
			} else {
				mbox = document.getElementById('messages_box')

				let div = document.createElement("div");
	            div.className = "mb-4";

				let child1 = document.createElement("div");
				let img = document.createElement("img");
				img.className = 'rounded-circle mr-1 me-2'
				img.alt = "Chris Wood"
				img.width = 40
				img.height = 40
				img.src = xhr.response['avatar']

				let user_span = document.createElement("span");
				user_span.innerHTML = xhr.response['user']

				let child2 = document.createElement("div");
				child1.appendChild(img)
				child1.appendChild(user_span)
				child2.className = 'flex-shrink-1 bg-light rounded py-2 px-3 mr-3 mt-2'
				child2.innerHTML = xhr.response['message_text']

				div.appendChild(child1)
				div.appendChild(child2)
				mbox.appendChild(div)
			}
        }
    } else {
		body.innerHTML = 'Нельзя отправить пустое сообщение!'
		show_toast()
    }
}
