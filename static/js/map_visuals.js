// JS will show syntax errors! 
"use strict";

function markers(){
	console.log('markers function');

	const infoWindow = new google.maps.InfoWindow;

	$('#show_directions').on('click', (evt) => {
		console.log('directions button listener to make markers')

		// taken from HTML data-route-id and grabs data from map_base.html
		const routeId = $(evt.target).data('routeId');

		$.get(`/map/${routeId}/directions`, (seg_info)=>{
			console.log('grabbing info about segment and plopping down markers')
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

				// mark all the start address
				const startMarker = new MarkerWithLabel({
					position:{
						lat: segment.start_lat,
						lng: segment.start_lng
					},
					map: window.map,
					draggable: false,
					// ${idx} to make labels
					labelContent: `1`,
					labelAnchor: new google.maps.Point(0, 35),
					labelClass: 'mapIcon'
				});


				startMarker.addListener('click', ()=>{
					infoWindow.close();
					infoWindow.setContent(segInfoContent);
					infoWindow.open(map, startMarker)
				});
			};

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

			const finalMarker = new MarkerWithLabel({
				position:{
					lat: finalStop.stop_lat,
					lng: finalStop.stop_lng
				},
				map: window.map,
				draggable: false,
				// ${idx} to make labels
				labelContent: `1`,
				labelAnchor: new google.maps.Point(0, 35),
				labelClass: 'mapIcon'
			});

			finalMarker.addListener('click', ()=>{
				infoWindow.close();
				infoWindow.setContent(segInfoContent);
				infoWindow.open(map, finalMarker);
			});

		});
	});
};
// actually calculating the route
// need to pass in route info from server via JSON
// need event listener on the show_directions button 
// AJAX to grab info about the segment... 
function calcRoute(){
	$('#show_directions').on('click', (evt) => {
		console.log('directions button listener to draw directions')

		// taken from HTML data-route-id and grabs data from map_base.html
		const routeId = $(evt.target).data('routeId');

		const directionsService = new google.maps.DirectionsService();

		$.get(`/map/${routeId}/directions`, (seg_info)=>{
			console.log('grabbing info about segs from server to draw route')
			// looping through list of segments

			let info = []
			for (const segment of seg_info){
				// get start and end's lat/lang AND mode of travel
				const leg = {
					origin: {
						lat: segment.start_lat,
						lng: segment.start_lng
					},
					destination: {
						lat: segment.stop_lat,
						lng: segment.stop_lng
					},
					travelMode: segment.mode.toUpperCase()
				};

				info.push(leg);
				
			}

			for (const leg of info){
				console.log('IN THE LEG LOOP??')

				// making new directionsRenderer for every segment = new route for every segment
				const directionsRenderer = new google.maps.DirectionsRenderer();
	    		directionsRenderer.setMap(window.map);

				directionsService.route(leg, (response, status) => {
					console.log('in the drawing route!');

					if (status === 'OK') {
						directionsRenderer.setDirections(response);
					} else {
						alert(`Directions request unsuccessful due to: ${status}`);
					}
				});
			}

		});
	});
}
