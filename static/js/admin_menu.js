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

	let xhr = new XMLHttpRequest()
	xhr.open('GET', '/account/admin/get_last_week_orders')
    xhr.send()
    xhr.responseType = 'json'

    xhr.onloadend = () => {
        if (xhr.response['ok'] == true){

            let ctx = document.getElementById("myChart").getContext("2d");
		    var myChart = new Chart(ctx, {
			    type: 'line',
			    data: {
			        labels: xhr.response['labels'],
			        datasets: [{
			            label: "Количество заказов",
			            borderColor: "#80b6f4",
			            pointBorderColor: "#80b6f4",
			            pointBackgroundColor: "#80b6f4",
			            pointHoverBackgroundColor: "#80b6f4",
			            pointHoverBorderColor: "#80b6f4",
			            pointBorderWidth: 10,
			            pointHoverRadius: 10,
			            pointHoverBorderWidth: 1,
			            pointRadius: 3,
			            fill: false,
			            borderWidth: 4,
			            data: xhr.response['values']
			        }]
			    },
			    options: {
			        legend: {
			            position: "bottom"
			        },
			        scales: {
			            yAxes: [{
			                ticks: {
			                    fontColor: "rgba(0,0,0,0.5)",
			                    fontStyle: "bold",
			                    beginAtZero: true,
			                    maxTicksLimit: 5,
			                    padding: 20
			                },
			                gridLines: {
			                    drawTicks: false,
			                    display: false
			                }
			            }],
			            xAxes: [{
			                gridLines: {
			                    zeroLineColor: "transparent"
			                },
			                ticks: {
			                    padding: 20,
			                    fontColor: "rgba(0,0,0,0.5)",
			                    fontStyle: "bold"
			                }
			            }]
			        }
			    }
			});

        }
    }

}
