// JS will show syntax errors! 
"use strict";

function markers(){
	console.log('markers function')

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

				const startMarker = new google.maps.Marker({
					position:{
						lat: segment.start_lat,
						lng: segment.start_lng
					},
					map: window.map,
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
};

