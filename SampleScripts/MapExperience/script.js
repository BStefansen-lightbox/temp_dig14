// Global Variables
const lbxAPIKey = ''
const URL = "https://api.lightboxre.com/v1/parcels/_adjacent/us/0201MABNPDBU5D2EGP08YA?commonOwnership='true'"
mapboxgl.accessToken = '';

// Initialize the map
const map = new mapboxgl.Map({
    container: 'map', // container ID in the HTML
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [-74.0060, 40.7128], // starting position [lng, lat]
    zoom: 9 // starting zoom
});

// Fetch API Data
const fetchData = async () => {
    try {
        const response = await fetch(URL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': lbxAPIKey
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json(); // Wait for the JSON data
        return data; // Return the parsed JSON data
    } catch (error) {
        console.error("Failed to fetch data:", error);
    }
};

function wktToGeoJSON(wkt) {
    const coords = wkt.match(/POLYGON \(\((.*?)\)\)/)[1].split(', ').map(pair => {
        const parts = pair.split(' ');
        return [parseFloat(parts[0]), parseFloat(parts[1])]; // Convert to [lng, lat]
    });
    return {
        type: "Polygon",
        coordinates: [coords] // GeoJSON polygons are arrays of LinearRing coordinate arrays
    };
}

// Call fetchData and handle the data
fetchData().then(data => {
    if (data) {
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
        
        // Add parcels as a new layer to the map
        map.on('load', function() {
            map.addSource('parcels', {
                type: 'geojson',
                data: geojsonData
            });
        
            map.addLayer({
                id: 'parcels-layer',
                type: 'fill',
                source: 'parcels',
                paint: {
                    'fill-color': '#FF0000',
                    'fill-opacity': 0.4
                }
            });

            console.log(JSON.stringify(geojsonData, null, 2));
        
            // Calculate the bounds from the GeoJSON data
            const bounds = new mapboxgl.LngLatBounds();
            geojsonData.features.forEach(feature => {
                feature.geometry.coordinates.forEach(coord => {
                    bounds.extend(coord);
                });
            });
        
            // Fit the map to the bounds with an animation
            map.fitBounds(bounds, {
                padding: 20, // Padding around the bounds
                duration: 2000 // Duration of the animation, in milliseconds
            });
        });
    }
}).catch(error => {
    console.error("Error fetching data:", error);
});



