// JS will show syntax errors! 
"use strict";

// this function called in homepage.html inside API connection
function initMap(){ 

	const map = new google.maps.Map(
	document.getElementById("map"),
	{
		// HB coordinates
		center: {lat: 37.601773, lng: -122.202870},
		zoom: 11
	})

	const infoWindow = new google.maps.InfoWindow;

	$('#show_directions').on('click', (evt) => {

		// taken from HTML data-route-id and grabs data from map_base.html
		const routeId = $(evt.target).data('routeId');

		$.get(`/map/${routeId}/directions`, (seg_info)=>{
			// looping through list of segments
			for (const segment of seg_info){
				// set the info in the window
				
				const segInfoContent = (
				`<div class="window-content"
								<ul class="seg-info">
					            <li><b>Stop order: </b>${segment.orderNum}</li>
					            <li><b>Mode of transportation: </b>${segment.mode}</li>
					          	</ul>
					        </div>`
		        );

				const startMarker = new google.maps.Marker({
					position:{
						lat: segment.start_lat,
						lng: segment.start_lng
					},
					map: map,
				});

				startMarker.addListener('click', ()=>{
					infoWindow.close();
					infoWindow.setContent(segInfoContent);
					infoWindow.open(map, startMarker)
				});
			}

			// last stop/final destination
			const finalStop = seg_info[seg_info.length - 1];

			const segInfoContent = (
				`<div class="window-content"
								<ul class="seg-info">
					            <li><b>Stop order: </b>${finalStop.orderNum}</li>
					            <li><b>Mode of transportation: </b>${finalStop.mode}</li>
					          	</ul>
					        </div>`
		        );

			const finalMarker = new google.maps.Marker({
				position:{
					lat: finalStop.stop_lat,
					lng: finalStop.stop_lng
				},
				map: map,
			});

			finalMarker.addListener('click', ()=>{
				infoWindow.close();
				infoWindow.setContent(segInfoContent);
				infoWindow.open(map, finalMarker)
			});

		});
	});
	$('#add_stop').on('click', (evt)=>{
		evt.preventDefault();
		evt.stopPropagation();
		// pointing at add_stop button
		const button = document.getElementById('add_stop');
		// grabbing unordered list of stops
		const stopList = document.getElementById('stop_list');

		stopList.append(`
		<li>
			<input name="stop" type="text" value="{{ route.segments[0].stop_address if route else '' }}"placeholder="Search stop">

				<select name="mode_stop">
					{% if route: %}
					<option value="{{ route.segments[0].mode.mode }}">{{ route.segments[0].mode.mode.title() }}</option> 
					{% else %}
					<option value="driving">Driving</option> {# google takes in driving #}
					<option value="walking">Walking</option> {# google takes in walking #}
					<option value="bicycling">Bicycling</option> {# google takes in bicycling #}
					<option value="transit">Public Transportation</option> {# google takes in transit #}
					{% endif %}
				</select>
				<input name="seg_order_stop" type="number" min="1" value="{{ route.segments[0].order_num if route else '' }}"placeholder="Stop order">

				{% if route %}
					<span name="duration">Distance: {{ seg_info['Segment 1']['distance']['text'] }}</span>

					<span name="duration">Duration: {{ seg_info['Segment 1']['duration']['text'] }} </span>
				{% endif %}
				{% if not route %}
				{# button to add stops #}
				<button id='add_stop'>+</button>
			</li>
			`)
	});
};
