// JS will show syntax errors! 
"use strict";

function dynamicForm() {


	$('#add_stop').on('click', (evt) => {

		// pointing at add_stop button
		const button = document.getElementById('add_stop');
		// // grabbing unordered list of stops
		// const stopList = document.getElementById('stop_list');
		// console.log(stopList);
		$('#stop_list').append(`
		<li>
			<input name="stop" type="text" class="stop_address" placeholder="Search stop">

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

	// submitting route name, address, mode, stop order
	$('#submit').on('click', async (evt)=>{
		event.preventDefault();

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
	});

	// handle making multiple stop thingies after picking which route to look at!

	
};

// calls dynamicForm function!! 
$(document).ready(function() {
	dynamicForm();

// 
	$('a.route').on('click', (evt) => {
		const routeId = $(evt.target).data('routeId');
		console.log(routeId);

		$.get(`/map/${routeId}`, (resp) =>{
			console.log(resp)
			console.log(resp.segment_1.mode)

			// populating route name
			$('#name').val(resp.routeName)
			// populating start address
			$('#start').val(resp.segment_1.start)
			// populate stop info
			$('#stop').val(resp.segment_1.stop)
			$('#mode_stop').html(`<option value="${resp.segment_1.mode}">${resp.segment_1.mode}</option> `)
			$('#seg_order_stop').val(resp.segment_1.order)

			// what to add as many stop list ele's as there are stops
			// insert data INTO the stops with `${stuff}`
			// TODO: figure out what to loop through. segment 2 and beyond really. 
			for (const info of Object.keys(resp)){

				
				if (info !== 'routeName' && info !== 'segment_1'){
					$('#stop_list').append(`
								<li>
									<input name="stop" type="text" class="stop_address" placeholder="Search stop">

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
				}	
			};
		});
	});
});
