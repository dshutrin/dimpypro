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


edit_github_link_func = () => {
	let input = document.createElement('input')
	input.className = 'form-control'
	input.placeholder = 'Введите новую ссылку'
	input.setAttribute('id', 'new_github_link_input')

	document.getElementById('empty_link_div').replaceWith(input)

	let button = document.createElement('button')
	button.className = 'btn btn-primary'
	button.setAttribute('id', 'send_new_github_link')
	button.setAttribute('onclick', 'send_new_github_link()')


	let back_button = document.createElement('button')
	back_button.className = 'btn btn-primary'
	back_button.setAttribute('id', 'back_button')
	back_button.setAttribute('onclick', 'back_link()')


		let svg = document.createElementNS("http://www.w3.org/2000/svg", 'svg')
	    svg.setAttribute('width', '20');
	    svg.setAttribute('height', '20');
		svg.setAttribute('fill', "currentColor");
		svg.setAttribute('viewBox', "0 0 16 16");
		svg.className="bi-check-lg"
		let iconPath = document.createElementNS(
		    'http://www.w3.org/2000/svg',
		    'path'
		);
		iconPath.setAttribute(
		    'd',
		    "M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"
		);
		svg.appendChild(iconPath)

	back_button.appendChild(svg)
	document.getElementById('link_form').insertBefore(back_button, document.getElementById('link_form').firstChild);

	svg = document.createElementNS("http://www.w3.org/2000/svg", 'svg')
    svg.setAttribute('width', '20');
    svg.setAttribute('height', '20');
	svg.setAttribute('fill', "currentColor");
	svg.setAttribute('viewBox', "0 0 16 16");
	svg.className="bi-check-lg"
	iconPath = document.createElementNS(
	    'http://www.w3.org/2000/svg',
	    'path'
	);
	iconPath.setAttribute(
	    'd',
	    "M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z"
	);
	svg.appendChild(iconPath)
	button.appendChild(svg)
	document.getElementById('edit_github_link').replaceWith(button)
}


back_link = () => {
	console.log('---------')
}


send_new_github_link = () => {
	let new_link = document.getElementById('new_github_link_input').value
	if (new_link.startsWith('https://github.com/') || new_link == '') {

		let order_id = document.getElementById('order_id_input').value
		let xhr = new XMLHttpRequest()
		xhr.open('POST', '/account/admin/order/' + order_id + '/set_git_link')
		xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val())
	    xhr.send(new_link)
	    xhr.responseType = 'json'

	    xhr.onloadend = () => {

	        if (xhr.response['ok'] == true){
				back_link()
				$('#linkError').hide()
	        } else {
				$('#linkError').show()
	        }

	    }

	} else {
		$('#linkError').show()
	}
}
