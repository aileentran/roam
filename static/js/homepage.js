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
		zoom: 18
	})
	const infoWindow = new google.maps.InfoWindow;

	// if allowed/able to get device's location
	if (navigator.geolocation){
		// getting device's position
		navigator.geolocation.getCurrentPosition((position) => {
			const pos = {
				lat: position.coords.latitude,
				lng: position.coord.longitude
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

	// Seachbox info!

	 // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }
      var icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      // Create a marker for each place.
      markers.push(new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        position: place.geometry.location
      }));

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
	}


	
	


};