var map;
var UKRAINE_BOUNDS = {
    north: 52.734444,
    south: 43.391111,
    west: 21.963889,
    east: 40.58056,
};
var ajaxRequestIsProcessing = false;

function CenterControl(controlDiv, map) {

    var controlUI = document.createElement('div');
    controlUI.className = 'create-marker-ui';
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.border = '2px solid #fff';
    controlUI.style.borderRadius = '3px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '22px';
    controlUI.style.marginTop = '35px';
    controlUI.style.marginLeft = '7px';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to create a marker';
    controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '20px';
    controlText.style.lineHeight = '43px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.style.fontWeight = '30px';
    controlText.innerHTML = 'CREATE MARKER';
    controlUI.appendChild(controlText);


    controlUI.addEventListener('click', function (event) {
        $(".create-markerDiv").modalForm({
            formURL: 'create/'
        });
    });
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        restriction: {
            latLngBounds: UKRAINE_BOUNDS,
            strictBounds: false,
        },
        zoom: 11,
        styles: [
            {
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#212121"
                    }
                ]
            },
            {
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "lightness": -15
                    },
                    {
                        "weight": 1.5
                    }
                ]
            },
            {
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#757575"
                    }
                ]
            },
            {
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#212121"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#757575"
                    }
                ]
            },
            {
                "featureType": "administrative.country",
                "elementType": "labels.text",
                "stylers": [
                    {
                        "color": "#26001d"
                    },
                    {
                        "weight": 8
                    }
                ]
            },
            {
                "featureType": "administrative.country",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#fcfcfc"
                    }
                ]
            },
            {
                "featureType": "administrative.locality",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#bdbdbd"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#757575"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#181818"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#616161"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#1b1b1b"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#2c2c2c"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#8a8a8a"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#373737"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#3c3c3c"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#4e4e4e"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#616161"
                    }
                ]
            },
            {
                "featureType": "transit",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#757575"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#000000"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#535353"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#3d3d3d"
                    }
                ]
            }
        ]
    });

    var geocoder = new google.maps.Geocoder;
    var infowindow = new google.maps.InfoWindow;

    $(document).ready(function () {
        geocodeLatLng(geocoder, map, infowindow);
    });

    navigator.geolocation.getCurrentPosition(function (position) {
        var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        map.setCenter(pos);
    });
    var centerControlDiv = document.createElement('div');
    centerControlDiv.className = "create-markerDiv";
    var centerControl = new CenterControl(centerControlDiv, map);
    centerControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(centerControlDiv);
}

function geocodeLatLng(geocoder, map, infowindow) {
    navigator.geolocation.getCurrentPosition(function (position) {
        var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        geocoder.geocode({'location': pos}, function (results, status) {
            if (status === 'OK') {
                if (results[0]) {
                    map.setZoom(11);
                    var userLocationInfo = results[0]['address_components'][4]['long_name'];
                    console.log(userLocationInfo)
                } else {
                    window.alert('Could not find your location');
                }
            } else {
                window.alert('Geocoder failed due to: ' + status);
            }
        });
    });
}

function displayMarkerInfo(marker_entity) {
    let markerId = marker_entity.get('id');
    let dashIndex = markerId.indexOf('-');
    markerId = markerId.substr(
        dashIndex + 1, markerId.length - dashIndex
    );
    markerId = parseInt(markerId);
    let data = {
        'marker_id': markerId
    };
    $.ajax({
        method: 'GET',
        url: '/map/marker_info/',
        data: data,
        dataType: 'html',
        beforeSend: function () {
            $('html, body').css("cursor", "wait");
        },
        success: function (response) {
            $('html, body').css("cursor", "auto");
            $.fancybox.open(response);
        },
        error: function (error) {
            $('html, body').css("cursor", "auto");
            console.log(error);
            alert('An error occured while loading page. Try later.');
        }
    })
}


