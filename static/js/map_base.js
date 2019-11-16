// What does this do? 
"use strict";

// this function called in homepage.html inside API connection
function initMap(){
	// Returns Geolocation object, gives Web content access to location of devide = get user's current location! 
	const map = new google.maps.Map(
	document.getElementById("map"),
	{
		// HB coordinates
		center: {lat: 37.601773, lng: -122.202870},
		zoom: 11
	})
	const infoWindow = new google.maps.InfoWindow;

	// if allowed/able to get device's location
	if (navigator.geolocation){
		// getting device's position
		navigator.geolocation.getCurrentPosition((position) => {
			const pos = {
				lat: position.coords.latitude,
				lng: position.coords.longitude
			};

			infoWindow.setPosition(pos);
			infoWindow.setContent("Current location");
			infoWindow.open(map);
			map.setCenter(pos);
		}
			);
	} else {
		// not allowed or not able to access device's location
		return "We cannot access your current location. Please input your address." 
	}

	

};
