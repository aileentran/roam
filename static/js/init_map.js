// JS will show syntax errors! 
"use strict";

// this function called in homepage.html inside API connection
function initMap(){ 
	console.log('initializing map')

	window.map = new google.maps.Map(
	document.getElementById("map"),
	{
		// SF Bay coordinates
		center: {lat: 37.601773, lng: -122.202870},
		zoom: 11
	})

	// adds live traffic layer
	// const trafficLayer = new google.maps.TrafficLayer();
 //  	trafficLayer.setMap(map);
	
};