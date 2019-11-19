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
			console.log(seg_info)
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
			console.log(finalStop);

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
