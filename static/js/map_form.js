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
			`);
	});

	// submitting route name, address, mode, stop order
	$('#submit').on('click', async (evt)=>{
		event.preventDefault();

		// grabbing info from HTML
		const routeName = document.getElementById('name').value;
		const start = document.getElementById('start').value;
		const stopList = document.getElementById('stop_list');
		const stopInfo = stopList.getElementsByTagName('li');

		let stopEle = {};

		// looping through stop list and extracting ALL inputs of each type
		for (const stop of stopInfo){
			stopEle['address'] = document.getElementsByClassName('stop_address');
			stopEle['mode'] = document.getElementsByClassName('mode_stop');
			stopEle['stop order'] = document.getElementsByClassName('stop_order');
		};

		// looping through all addresses and saving string to list 
		const stopAddressValues = [];
		for (const address of stopEle['address']){
			stopAddressValues.push(address.value);
		};

		// looping through all modes and saving string to list
		const modeValues = [];
		for (const mode of stopEle['mode']){
			modeValues.push(mode.value)
		};

		// loop through all stop orders and saving integer to list
		const stopOrderValues = [];
		for(const order of stopEle['stop order']){
			stopOrderValues.push(order.value)
		};

		console.log(stopOrderValues);

		const data = {
			name: routeName,
			startAddress: start, 
			stopAddress: stopAddressValues,
			mode: modeValues,
			stopOrder: stopOrderValues
		};

		// ex: how to package stop info 
		// {0: {}, 1: {}, 2:{}}

		
		// const response = await fetch('/save_route', 
		// 	{ 	
		// 		method: 'POST',
		// 		body: JSON.stringify(data), 
		// 		headers: {'Content-Type': 'application/json'} 
		// 	}
		// );
		// const response2 = await response.json()
		// console.log(response2)
		$.post('/save_route', data, (resp) => {
			console.log(resp)
			// with the response we can show stuff on the page
			// such as showing "it was successfully saved"

		})
	});
};

// calls dynamicForm function!! 
$(document).ready(function() {
	dynamicForm();
});
