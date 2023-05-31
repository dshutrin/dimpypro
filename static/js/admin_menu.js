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
	clear_menu();
	$('#bonus_history_admin_menu').addClass('active');
}


gen_diagram = () => {

	const CHART_COLORS = {
		red: 'rgb(255, 99, 132)',
		orange: 'rgb(255, 159, 64)',
		yellow: 'rgb(255, 205, 86)',
		green: 'rgb(75, 192, 192)',
		blue: 'rgb(54, 162, 235)',
		purple: 'rgb(153, 102, 255)',
		grey: 'rgb(201, 203, 207)'
	};

	let xhr = new XMLHttpRequest()
	xhr.open('GET', '/account/admin/get_last_week_orders')
    xhr.send()
    xhr.responseType = 'json'

    xhr.onloadend = () => {
        if (xhr.response['ok'] == true){

            console.log(xhr.response)

			// Заказы за неделю
            let ctx = document.getElementById("myChart").getContext("2d");
		    var myChart = new Chart(ctx, {
			    type: 'line',
			    data: {
			        labels: xhr.response['labels'],
			        datasets: [{
			            cubicInterpolationMode: 'monotone',
			            fill: false,
			            tension: 0.4,
			            borderColor: '#ff6384',
			            label: "Количество заказов",
			            data: xhr.response['values']
			        }]
			    },
			    options: {
			        legend: {
			            position: "bottom"
			        },
			        scales: {
			            y: {
					        display: true,
					        title: {
					          display: true,
					          text: 'Value'
					        },
					        suggestedMin: 0,
					        suggestedMax: 200
					    },
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

			// Круговая диаграмма
			ctx = document.getElementById("statusChart").getContext("2d");
			var sChart = new Chart(ctx, {
				type: 'doughnut',
				data: {
					labels: ['Подан', 'Принят', 'В разработке', 'Требуется проверка', 'Устанавливается', 'Готово'],
					datasets: [
						{
							label: 'Dataset 1',
							data: [
								xhr.response['statuses']['Подан'],
								xhr.response['statuses']['Принят'],
								xhr.response['statuses']['В разработке'],
								xhr.response['statuses']['Требуется проверка'],
								xhr.response['statuses']['Устанавливается'],
								xhr.response['statuses']['Готово'],
							],
							backgroundColor: ['rgb(201, 203, 207)', 'rgb(255, 205, 86)', 'rgb(54, 162, 235)', 'rgb(255, 99, 132)', 'rgb(153, 102, 255)', 'rgb(75, 192, 192)']
						}
					]
				},
				options: {
					responsive: true,
					plugins: {
						legend: {
							position: 'left',
						},
						title: {
							display: true,
							text: 'Chart.js Doughnut Chart'
						}
					}
				},
			});

        }
    }

}

show_status_toast = (code, title, desc) => {
	document.getElementById('status_change_title').innerHTML = title
	document.getElementById('status_change_text').innerHTML = desc

	let toast = document.getElementById('liveToast2')
	toast = new bootstrap.Toast(toast)
	toast.show()
};

change_order_status = () => {
	let status_id = document.getElementById('status_select').value
	let order_id = document.getElementById('order_id_input').value

	let xhr = new XMLHttpRequest()
	xhr.open('GET', '/account/admin/order/' + order_id + '/set_status/' + status_id)
    xhr.send()
    xhr.responseType = 'json'

    xhr.onloadend = () => {
        console.log(xhr.response)
		if (xhr.response['ok'] == true) {
			show_status_toast(true, 'Успех!', 'Статус заказа изменён на "' + xhr.response['status'] + '"')
		} else {

		}
    }
}

(function () {
    if (typeof EventTarget !== "undefined") {
        let func = EventTarget.prototype.addEventListener;
        EventTarget.prototype.addEventListener = function (type, fn, capture) {
            this.func = func;
            if(typeof capture !== "boolean"){
                capture = capture || {};
                capture.passive = false;
            }
            this.func(type, fn, capture);
        };
    };
}());
