var image = {
    url: "https://png.pngtree.com/svg/20170602/b7c3ca6e9e.svg",
    scaledSize: new google.maps.Size(50, 50)
}
if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(position =>{
        console.log(position);
        var marker1 = new google.maps.Marker({
            position: {lat: position.coords.latitude, lng: position.coords.longitude},
            icon: image,
            map: map,
            title: 'Hello World!',
	        animation: google.maps.Animation.BOUNCE,
	        draggable: false
        });
    });
}
else{
    alert("Geolocation is off on your computer");
}