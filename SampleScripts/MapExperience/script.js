// Initialize the map
const lbxAPIKey = 'ATFY7foMHsxT2wsgBD5Ovmwy6YvPWtDh'
mapboxgl.accessToken = 'pk.eyJ1IjoiZHJhbWJhcnJhbi1sYngiLCJhIjoiY2x2d3NoODdnMmJqbDJzbWczOXk5bHVrMCJ9.r21DV-PhxRlvISwDyr0bFw';
const map = new mapboxgl.Map({
    container: 'map', // container ID in the HTML
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [-74.0060, 40.7128], // starting position [lng, lat]
    zoom: 9 // starting zoom
});

function fetchData(parcelId) {
    const URL = `https://api.lightboxre.com/v1/parcels/_adjacent/us/${parcelId}?commonOwnership='true'`
    fetch(URL, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': lbxAPIKey
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            console.log(data);

            const geojsonData = {
                type: "FeatureCollection",
                features: data.parcels.map(parcel => ({
                    type: "Feature",
                    geometry: wktToGeoJSON(parcel.location.geometry.wkt), // Convert WKT to GeoJSON
                    properties: {
                        id: parcel.id,
                        apn: parcel.parcelApn,
                        owner: parcel.owner.names ? parcel.owner.names[0].fullName : "No owner data",
                        address: parcel.location.streetAddress
                    }
                }))
            };

            console.log(geojsonData);
            
            // Ensure the map is loaded before adding sources and layers
            if (map.isStyleLoaded()) {
                setupMapEvents(geojsonData);
            } else {
                map.on('load', () => setupMapEvents(geojsonData));
            }
        }
    })
    .catch(error => {
        console.error("Error fetching data:", error);
    });
}

function wktToGeoJSON(wkt) {
    var wicket = new Wkt.Wkt();
    wicket.read(wkt);
    return wicket.toJson(); // Converts WKT to a GeoJSON object
}

function setupMapEvents(geojsonData) {
    // Adding event listeners directly within this function
    map.on('click', 'parcels-fill', function(e) {
        if (e.features.length > 0) {
            var feature = e.features[0];
    
            var popupContent = `
                <h3>Parcel Information</h3>
                <p><strong>ID:</strong> ${feature.properties.id}</p>
                <p><strong>APN:</strong> ${feature.properties.apn}</p>
                <p><strong>Owner:</strong> ${feature.properties.owner}</p>
                <p><strong>Address:</strong> ${feature.properties.address}</p>
            `;
    
            new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(popupContent)
                .addTo(map);
        }
    });

    map.on('mouseenter', 'parcels-fill', function() {
        map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', 'parcels-fill', function() {
        map.getCanvas().style.cursor = '';
    });

    // Add data to the map
    addDataToMap(geojsonData);
}

function addDataToMap(geojsonData) {
    function assignRandomColors(geojsonData) {
        const colorsUsed = {}; // Object to keep track of colors that have already been used
    
        geojsonData.features.forEach(feature => {
            let color;
            do {
                color = `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
            } while (colorsUsed[color]); // Ensure this color hasn't already been used
    
            colorsUsed[color] = true; // Mark this color as used
            feature.properties.randomColor = color;
        });
    
        return geojsonData;
    }

    geojsonData = assignRandomColors(geojsonData);

    // Ensure the 'parcels' source is added only once
    if (!map.getSource('parcels')) {
        map.addSource('parcels', {
            type: 'geojson',
            data: geojsonData
        });
    } else {
        map.getSource('parcels').setData(geojsonData);
    }

    geojsonData.features.forEach(feature => {
        feature.properties.randomColor = `#${Math.floor(Math.random()*16777215).toString(16)}`;
    });
    // Add the fill layer for the parcels
    if (!map.getLayer('parcels-fill')) {
        map.addLayer({
            id: 'parcels-fill',
            type: 'fill',
            source: 'parcels',
            paint: {
                'fill-color': ['get', 'randomColor'],  // Red fill color
                'fill-opacity': 0.4       // Slightly transparent
            }
        });
    }

    // Add the line layer for the parcels to create an outline
    if (!map.getLayer('parcels-line')) {
        map.addLayer({
            id: 'parcels-line',
            type: 'line',
            source: 'parcels',
            layout: {},
            paint: {
                'line-color': '#000',     // Black line color
                'line-opacity': 0.5,
                'line-width': 1          // Line width in pixels
            }
        });
    }

    fitMapToBounds(geojsonData);
}

function fitMapToBounds(geojsonData) {
    const bounds = new mapboxgl.LngLatBounds();
    geojsonData.features.forEach(feature => {
        feature.geometry.coordinates[0].forEach(coord => {
            bounds.extend(coord);
        });
    });

    map.fitBounds(bounds, {
        padding: 20,
        duration: 2000
    });
}

function main() {
    document.addEventListener('DOMContentLoaded', function () {
        const parcelTypeSelect = document.getElementById('parcel-type');
    
        // Add event listener for change event
        parcelTypeSelect.addEventListener('change', function () {
            selectedValue = parcelTypeSelect.value;
            fetchData(selectedValue);
        });
    });
}


main();
