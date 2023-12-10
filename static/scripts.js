var map = L.map('map').setView([38.9637, 35.2433], 7);
var markers = L.markerClusterGroup();

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

function addReportToMap(report) {
    var marker = L.marker([report.latitude, report.longitude])
        .bindPopup(`Message: ${report.message}, Phone: ${report.phone}, Address: ${report.address}`);
    markers.addLayer(marker);
    map.addLayer(markers);
}

function fetchAndDisplayReports() {
    fetch('/reports')  // This route serves both manual reports and tweets
        .then(response => response.json())
        .then(data => {
            data.forEach(report => addReportToMap(report));
        });
}

function showLoadingIndicator(show) {
    var indicator = document.getElementById('loading-indicator');
    if (show) {
        indicator.classList.add('visible');
        indicator.classList.remove('hidden');
    } else {
        indicator.classList.add('hidden');
        indicator.classList.remove('visible');
    }
}

document.getElementById('report-form').addEventListener('submit', function (e) {
    e.preventDefault();
    showLoadingIndicator(true);

    var message = document.getElementById('message').value;
    var phone = document.getElementById('phone').value;
    var address = document.getElementById('address').value;

    geocodeAddress(address, function (lat, lon) {
        var report = {
            message: message,
            phone: phone,
            address: address,
            latitude: lat,
            longitude: lon
        };

        fetch('/report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(report)
        })
            .then(response => response.json())
            .then(data => {
                addReportToMap(report);
                showLoadingIndicator(false);
                alert('Report submitted successfully');
            })
            .catch(error => {
                console.error('Error:', error);
                showLoadingIndicator(false);
                alert('Failed to submit report');
            });
    });
});

function geocodeAddress(address, callback) {
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${address}`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                callback(data[0].lat, data[0].lon);
            } else {
                alert('Address not found');
                showLoadingIndicator(false);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Geocoding failed');
            showLoadingIndicator(false);
        });
}

// Update the map with the latest data periodically
setInterval(fetchAndDisplayReports, 300000); // Refresh every 5 minutes
