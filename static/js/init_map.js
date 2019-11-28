// JS will show syntax errors! 
"use strict";

// this function called in homepage.html inside API connection
function initMap(){ 

	window.map = new google.maps.Map(
	document.getElementById("map"),
	{
		// HB coordinates
		center: {lat: 37.601773, lng: -122.202870},
		zoom: 11
	})
	
};