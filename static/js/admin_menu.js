clear_menu = () => {
	let items = ['main_admin_menu', 'bonuses_admin_menu', 'orders_admin_menu', 'bonus_history_admin_menu']
	items.forEach((item) => {
		$('#'+item).removeClass('active')
	})
}

set_main_admin_menu = () => {
	clear_menu()
	$('#main_admin_menu').addClass('active')
}

set_bonuses_admin_menu = () => {
	clear_menu()
	$('#bonuses_admin_menu').addClass('active')
}

set_orders_admin_menu = () => {
	clear_menu()
	$('#orders_admin_menu').addClass('active')
}

set_history_admin_menu = () => {
	clear_menu()
	$('#bonus_history_admin_menu').addClass('active')
}

gen_diagram = () => {
	let ctx = document.getElementById("myChart").getContext("2d");
    let myChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
            datasets: [
                {
                    label: "Среднее время выполнения заказа",
                    data: [2, 9, 3, 17, 6, 3, 7],
                    backgroundColor: "rgba(153,205,1,0.6)",
                }
            ],
        },
    });
}
