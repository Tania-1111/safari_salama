// Shared JS for role landing pages
function initMap() {
    // simple placeholder map initialization
    const el = document.getElementById('map');
    if (!el) return;
    el.textContent = 'Map ready (provide Google Maps API key in views)';
}

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-trip');
    const endBtn = document.getElementById('end-trip');
    const appData = document.getElementById('app-data');
    const busId = appData ? appData.dataset.busId : null;

    let gpsWatchId = null;

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    async function postLocation(payload) {
        try {
            const csrftoken = getCookie('csrftoken');
            await fetch('/driver/location/update/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken || ''
                },
                body: JSON.stringify(payload)
            });
        } catch (e) {
            console.error('Error posting location', e);
        }
    }

    function startGPSTracking() {
        if (!navigator.geolocation) {
            alert('Geolocation not supported');
            return;
        }

        gpsWatchId = navigator.geolocation.watchPosition(position => {
            const payload = {
                bus_id: busId || null,
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy: position.coords.accuracy,
                speed: position.coords.speed,
                heading: position.coords.heading
            };
            postLocation(payload);
        }, err => {
            console.error('Geolocation error', err);
        }, { enableHighAccuracy: true, maximumAge: 5000, timeout: 10000 });
    }

    function stopGPSTracking() {
        if (gpsWatchId !== null) {
            navigator.geolocation.clearWatch(gpsWatchId);
            gpsWatchId = null;
        }
    }

    if (startBtn) startBtn.addEventListener('click', () => {
        startBtn.disabled = true;
        startBtn.textContent = 'Trip started';
        startGPSTracking();
        alert('Trip started — GPS tracking will begin.');
    });

    if (endBtn) endBtn.addEventListener('click', () => {
        if (startBtn) startBtn.disabled = false;
        stopGPSTracking();
        alert('Trip ended.');
    });
});
