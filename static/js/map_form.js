// JS will show syntax errors! 
"use strict";

function dynamicForm() {


	$('#add_stop').on('click', (evt) => {
		console.log("clicked");

		// pointing at add_stop button
		// const button = document.getElementById('add_stop');
		// // grabbing unordered list of stops
		// const stopList = document.getElementById('stop_list');
		// console.log(stopList);
		$('#stop_list').append(`
		<li>
			<input name="stop" type="text" placeholder="Search stop">

				<select name="mode_stop">
					<option value="driving">Driving</option> {# google takes in driving #}
					<option value="walking">Walking</option> {# google takes in walking #}
					<option value="bicycling">Bicycling</option> {# google takes in bicycling #}
					<option value="transit">Public Transportation</option> {# google takes in transit #}
				</select>
				
				<input name="seg_order_stop" type="number" min="1" placeholder="Stop order">

				<button id='add_stop' type="button">+</button>
			</li>
			`);
	});

	// submitting route name, address, mode, stop order
	// $('#submit').on('click', (evt)=>{

	// });
};

// calls dynamicForm function!! 
$(document).ready(function() {
	dynamicForm();
});
