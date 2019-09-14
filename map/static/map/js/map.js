var map;
var currentPosition;
var UKRAINE_BOUNDS = {
    north: 52.734444,
    south: 43.391111,
    west: 21.963889,
    east: 40.58056,
};
function loadMarkers(clusterId) {
    $.ajax({
        type: "GET",
        url: '/map/',
        data: {
            'regionId': clusterId
        },
        success:function(response) {
            $("body").append(response);
        }
    });
}
function CreateMarkerControl(controlDiv, map) {
    var ajaxRequestIsProcessing = false;
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
    var createMarkerDiv = document.createElement('div');
    createMarkerDiv.className = "create-markerDiv";
    var createMarkerControl = new CreateMarkerControl(createMarkerDiv, map);
    createMarkerDiv.index = 1;
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(createMarkerDiv);
}
function geocodeLatLng(geocoder, map, infowindow) {
    navigator.geolocation.getCurrentPosition(function (position) {
        currentPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        geocoder.geocode({'location': currentPosition}, function (results, status) {
            if (status === 'OK') {
                if (results[0]) {
                    map.setZoom(11);
                    for (var i = 0; i < results.length; i++) {
						if (results[i].types[0] === "locality") {
							var region = results[i].address_components[2].short_name;
							$("input[name='location']").val(region);

						}
                    }
                    switch(region){
                        case "Львівська область":
                            loadMarkers(44);
                            mLvivska.setMap(null);
                            break;
                        case "Миколаївська область":
                            loadMarkers(28);
                            mMykolayivska.setMap(null);
                            break;
                        case "Тернопільська область":
                            loadMarkers(29);
                            mTernopilska.setMap(null);
                            break;
                        case "Житомирська область":
                            loadMarkers(30);
                            mZhytomyrska.setMap(null);
                            break;
                        case "Кіровоградська область":
                            loadMarkers(31);
                            mKirovohradska.setMap(null);
                            break;
                        case "Одеська область":
                            loadMarkers(32);
                            mOdeska.setMap(null);
                            break;
                        case "Волинська область":
                            loadMarkers(33);
                            mVolynska.setMap(null);
                            break;
                        case "Київська область":
                            loadMarkers(34);
                            mKyivska.setMap(null);
                            break;
                        case "Вінницька область":
                            loadMarkers(35);
                            mVinnytska.setMap(null);
                            break;
                        case "Донецька область":
                            loadMarkers(36);
                             mDonetska.setMap(null);
                             break;
                        case "Рівненська область":
                            loadMarkers(37);
                            mRivnenska.setMap(null);
                            break;
                        case "Чернівецька область":
                            loadMarkers(38);
                            mChernivetska.setMap(null);
                            break;
                        case "Дніпропетровська область":
                            loadMarkers(39);
                            mDnipropetrovska.setMap(null);
                            break;
                        case "Харківська область":
                            loadMarkers(40);
                            mKharkivska.setMap(null);
                            break;
                        case "Черкаська область":
                            loadMarkers(41);
                            mCherkaska.setMap(null);
                            break;
                        case "Закарпатська область":
                            loadMarkers(42);
                            mZakarpatska.setMap(null);
                            break;
                        case "Луганська область":
                            loadMarkers(43);
                            mLuhanska.setMap(null);
                            break;
                        case "Полтавська область":
                            loadMarkers(45)
                            mPoltavska.setMap(null);
                            break;
                        case "Хмельницька область":
                            loadMarkers(46);
                            mKhmelnytska.setMap(null);
                            break;
                        case "Автономна республіка Крим":
                            loadMarkers(47);
                            mCrimea.setMap(null);
                            break;
                        case "Запорізька область":
                            loadMarkers(48);
                            mZaporizka.setMap(null);
                            break;
                        case "Івано-Франківська область":
                            loadMarkers(49);
                            mIvanoFrankivska.setMap(null);
                            break;
                        case "Сумська область":
                            loadMarkers(50);
                            mSumska.setMap(null);
                            break;
                        case "Чернігівська область":
                            loadMarkers(51);
                            mChernihivska.setMap(null);
                            break;
                        case "Херсонська область":
                            loadMarkers(52);
                            mKhersonska.setMap(null);
                            break;
                    }
                } else {
                    window.alert('Could not find your location');
                }
            }else {
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


