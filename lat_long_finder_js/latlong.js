var geocoder = require('geocoder');

// Geocoding
geocoder.geocode("Kamta chinhat Lucknow", function ( err, data ) {
  console.log("Kamta")
  console.log(data.results[0].geometry.location.lat)
  console.log(data.results[0].geometry.location.lng)
});

geocoder.geocode(" Lucknow", function ( err, data ) {
  console.log("chinhat")
  console.log(data.results[0].geometry.location.lat)
  console.log(data.results[0].geometry.location.lng)
});
