// JS will show syntax errors! 
"use strict";

function dynamicForm() {

	console.log('dynamic form function')

	// autocomplete for start address
	// console.log('autocomplete for start address')

	// const startInput = document.getElementById('start');
	// const startOptions = {
	//   types: ['address']
	// };

	// const autocompleteStart = new google.maps.places.Autocomplete(startInput, startOptions);

	$('#add_stop').on('click', (evt) => {

		console.log('add stop button')
		// pointing at add_stop button
		const button = document.getElementById('add_stop');
		// // grabbing unordered list of stops
		// const stopList = document.getElementById('stop_list');
		// console.log(stopList);
		$('#stop_list').append(`
		<li>
			<input name="stop" id="stop" type="text" class="stop_address" placeholder="Search stop">

				<select name="mode_stop" class="mode_stop">
					<option value="driving">Driving</option> 
					<option value="walking">Walking</option> 
					<option value="bicycling">Bicycling</option> 
					<option value="transit">Public Transportation</option>
				</select>

				<input name="seg_order_stop" type="number" class="stop_order" min="1" placeholder="Stop order">
		</li>

		<span id="distance"></span>

		<span id="duration"></span>

		<span id="eta"></span>
			`);
	});



	// autocomplete for stop addresses

	// TODO: get added stops to autocomplete as well. 


	// const stopList = document.getElementById('stop_list');
	// console.log(stopList)

	// const stopInput = document.getElementById('stop');
	// const stopOptions = {
	//   types: ['address']
	// };

	// const autocompleteStop = new google.maps.places.Autocomplete(stopInput, stopOptions);

	// submitting route name, address, mode, stop order
	$('#submit').on('click', async (evt)=>{
		event.preventDefault();

		console.log('submit click event')

		// grabbing info from HTML
		const routeName = document.getElementById('name').value;
		const start = document.getElementById('start').value;
		const stopList = document.getElementById('stop_list');
		const addresses = document.getElementsByClassName('stop_address');
		const modes = document.getElementsByClassName('mode_stop');
		const stopOrder = document.getElementsByClassName('stop_order');

		// looping through all addresses and saving string to obj w/idx as key
		let stopAddressValues = {};
		for (const address in addresses){
			stopAddressValues[address] = addresses[address].value;
		};

		// converting obj into JSON string
		const stopAddressJSON = JSON.stringify(stopAddressValues);

		// looping through all modes and saving string to obj
		let modeValues = {};
		for (const mode in modes){
			modeValues[mode] = modes[mode].value;
		};
		// converting modeValues obj to JSON
		const modeJSON = JSON.stringify(modeValues);

		// loop through all stop orders and saving integer to obj w/idx as key
		let stopOrderValues = {};
		for(const order in stopOrder){
			stopOrderValues[order] = stopOrder[order].value;
		};

		// converting stopOrderValues to JSON
		const orderJSON = JSON.stringify(stopOrderValues);


		const data = {
			name: routeName,
			startAddress: start, 
			stopAddress: stopAddressJSON,
			mode: modeJSON,
			stopOrder: orderJSON
		};

		// maybe use this later to populate 
		$.post('/save_route', data, (resp) => {
			alert(resp);

		});

		// TODO: reload page to add new route to list??? 
	});	
};

// calls dynamicForm function!! 
$(document).ready(function() {
	dynamicForm();
});

// selecting a route and populating the form 
$('a.route').on('click', (evt) => {
	console.log('a.route event listener')

	const routeId = $(evt.target).data('routeId');

	$.get(`/map/${routeId}`, (resp) =>{
		console.log('ajax getting route id and populating form')
		// populating route name
		$('#name').val(resp.routeName)
		// populating start address
		$('#start').val(resp.segment_1.start)
		// populate stop info
		$('#stop').val(resp.segment_1.stop)
		$('#mode_stop').html(`<option value="${resp.segment_1.mode}">${resp.segment_1.mode}</option> `)
		$('#seg_order_stop').val(resp.segment_1.order)
		$('.distance').text(`Distance ${resp.segment_1.distance}`)
		$('.duration').text(`Time ${resp.segment_1.duration}`)

		// what to add as many stop list ele's as there are stops
		// insert data INTO the stops with `${stuff}` 

		// keeping track of total travel time for entire route
		let travelTime = 0;

		for (const info of Object.keys(resp)){
			
			if (info !== 'routeName' && info !== 'segment_1'){
				$('#stop_list').append(`
							<li>
								<input name="stop" type="text" class="stop_address" value="${resp[info].stop}" placeholder="Search stop">

									<select name="mode_stop" class="mode_stop">
										<option value="${resp[info].mode}">${resp[info].mode}</option>

									<input name="seg_order_stop" type="number" class="stop_order" min="1" value="${resp[info].order}"placeholder="Stop order">
									<span class="distance">Distance ${resp[info].distance}</span>

									<span class="duration">Time ${resp[info].duration}</span>
							</li>

						`);
			};
			
			// summing up total travel time
			if (info !== 'routeName'){
				const time = resp[info].durationInt;
				travelTime += time;
			}
		};

		// returning total travel time for route
		$('#total-time').text(`Travel time: ${travelTime} mins`);

		// const days = travelTime / (60 * 60 * 24);

		// travelTime = travelTime % (3600 * 24);
		// const hours = Math.round(travelTime / (60 * 60));

		// travelTime = travelTime % (60 * 60);
		// const min = Math.round(travelTime / 60);

		// if (days >= 1){
		// 	$(`#total-time`).text(`Travel time: ${days} day ${hours} hours ${min} mins`);
		// } else if (hours >= 1){
		// 	$(`#total-time`).text(`Travel time: ${hours} hours ${min} mins`)
		// } else {
		// 	$(`#total-time`).text(`Travel time: ${min} mins`)
		// }

		// $('.eta').text(`ETA: ${resp.segment_1.eta}`)

		// changing submit button to directions button
		$('#button-container').html(`<button
		 		type='button'
		 		id="show_directions"
		 		data-route-id="${routeId}"
		 	>Directions
		 	</button>`);

		// draws paths
		calcRoute();
	});
	// change submit button to directions = pins on map! 
	// maybe save room for update button??
});

// comparing all route travel times
$('#compare').on('click', (evt) =>{
	console.log('evt listener for comparing travel times button')
	// need to get routeId to get specific route's total travel time
 
	// gets python obj of routes as a string
	// isolate the route id
	const routeStr = $(evt.target).data('routes');

	// splitting the string to isolate the route id
	// first idx (idx = 0) is just '[<Route'
	// route id is first idx of lst at idx 1+
	const splitRouteId = routeStr.split('route id=');
	// isolating route id by making new list W/OUT '[<Route'
	const isoRouteId = splitRouteId.slice(1);
	console.log(isoRouteId);
		
	// iterating through equivalent of routeId ONLY IF FOR FIRST USER!!
	for (let info of isoRouteId ){
		console.log('looping through list of route info')
		
		// grabbing char at first index and converting it to a number
		const routeId = Number(info[0]);

		$.get(`/map/${routeId}`, (resp) =>{
			console.log('ajax req for comparison button')

			let travelTime = 0;

			// calculating total travel time for a route
			for (const info of Object.keys(resp)){
				if (info !== 'routeName'){
					const time = resp[info].seconds;
					travelTime += time;
				};
			}

			// converting seconds to days, hours, min
			// probably don't need days... 
			const days = travelTime / (60 * 60 * 24);

			travelTime = travelTime % (3600 * 24);
			const hours = Math.floor(travelTime / (60 * 60));

			travelTime = travelTime % (60 * 60);
			const min = Math.round(travelTime / 60);

			if (days === 1){
				$(`#travel-time-${routeId}`).text(`Travel time: ${days} day ${hours} hour ${min} mins`);
			} else if (days > 1){
				$(`#travel-time-${routeId}`).text(`Travel time: ${days} day ${hours} hours ${min} mins`);
			} else if (hours === 1){
				$(`#travel-time-${routeId}`).text(`Travel time: ${hours} hour ${min} mins`);
			} else if (hours > 1){
				$(`#travel-time-${routeId}`).text(`Travel time: ${hours} hours ${min} mins`);
			} else {
				$(`#travel-time-${routeId}`).text(`Travel time: ${min} mins`);
			}

		});
	}
});
