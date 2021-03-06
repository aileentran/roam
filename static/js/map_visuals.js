// JS will show syntax errors! 
"use strict";

function markers(){
	console.log('markers function');

	// const infoWindow = new google.maps.InfoWindow;

	$('#show_directions').on('click', (evt) => {
		console.log('directions button listener to make markers')

		// taken from HTML data-route-id and grabs data from map_base.html
		const routeId = $(evt.target).data('routeId');

		$.get(`/map/${routeId}/directions`, (seg_info)=>{
			console.log('grabbing info about segment and plopping down markers')

			// setting zoom function to encase ALL markers
			// create empty LatLngBounds object
			var bounds = new google.maps.LatLngBounds();

			// looping through list of segments
			for (const idx in seg_info){

				const segment = seg_info[idx];
				// customized markers based on address order
				const addressOrder = Number(idx) + 1;

				// mark all the start address
				const startMarker = new MarkerWithLabel({
					position:{
						lat: segment.start_lat,
						lng: segment.start_lng
					},
					map: window.map,
					draggable: false,
					labelContent: `${addressOrder}`,
					labelAnchor: new google.maps.Point(0, 35),
					labelClass: 'mapIcon'
				});


				// last stop/final destination
				const finalStop = seg_info[seg_info.length - 1];

				const finalMarker = new MarkerWithLabel({
					position:{
						lat: finalStop.stop_lat,
						lng: finalStop.stop_lng
					},
					map: window.map,
					draggable: false,
					// last address is always one more than the # of segs
					labelContent: `${seg_info.length + 1}`,
					labelAnchor: new google.maps.Point(0, 35),
					labelClass: 'mapIcon'
				});

				//extend the bounds to include each marker's position
	  			bounds.extend(startMarker.position);
	  			bounds.extend(finalMarker.position);

	  			//now fit the map to the newly inclusive bounds
				map.fitBounds(bounds);
			};
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

		$('#users-routes').hide();

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
				const directionsRenderer = new google.maps.DirectionsRenderer({
					suppressMarkers: true,
					suppressBicyclingLayer: true,
					preserveViewport: true
				});
	    		directionsRenderer.setMap(window.map);

	    		directionsRenderer.setPanel(document.getElementById('directionsPanel'));

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
