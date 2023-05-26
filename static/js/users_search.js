search_users = () => {
    let value = document.getElementById('id_data').value
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    let xhr = new XMLHttpRequest()
    if (value)
        xhr.open('POST', '/account/admin/bonuses/get_users/' + value)
    else
        xhr.open('POST', '/account/admin/bonuses/get_users/ALL_USERS')
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.send()
    xhr.responseType = 'json'

    get_user_card = (username, id) => {
        let div = document.createElement("div");
        div.className = "col-3";

        let card = document.createElement("div");
        card.className = "card";

        let top = document.createElement("div");
        top.className = "card-body fs-4";
        top.innerHTML = username

        let footer = document.createElement("div");
        footer.className = "card-footer text-end";

        let link = document.createElement("a");
        link.className = 'btn btn-primary'
        link.href = '/account/admin/bonuses/' + id
        link.innerHTML = 'Выбрать'

        card.appendChild(top)
        footer.appendChild(link)
        card.appendChild(footer)
        div.appendChild(card)
        document.getElementById("users_block").appendChild(div);
    }

	clear_users_block = () => {
		let e = document.getElementById("users_block")
	    let child = e.lastElementChild;
	    while (child) {
	        e.removeChild(child);
	        child = e.lastElementChild;
	    }
	}

    xhr.onload = () => {
        clear_users_block()
        xhr.response['objects'].forEach((user) => {
            get_user_card(user['username'], user['id'])
        })
    }
}
