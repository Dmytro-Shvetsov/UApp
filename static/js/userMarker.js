var image = {
    url: "static/images/UserMarker.png",
    scaledSize: new google.maps.Size(105, 105)
};
if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(position =>{
        var marker1 = new google.maps.Marker({
            position: {lat: position.coords.latitude, lng: position.coords.longitude},
            icon: image,
            map: map,
            title: 'It is you',
	        animation: google.maps.Animation.BOUNCE,
	        draggable: false
        });
    });
}
else{
    alert("Geolocation is off on your computer");
}