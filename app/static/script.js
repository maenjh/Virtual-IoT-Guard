const ws = new WebSocket(`ws://${window.location.host}/ws`);
const connectionStatus = document.getElementById('connectionStatus');
const lightBulb = document.getElementById('lightBulb');
const lightStatusText = document.getElementById('lightStatusText');
const logList = document.getElementById('logList');

let lightTimeout;

ws.onopen = () => {
    connectionStatus.textContent = 'Connected';
    connectionStatus.classList.add('connected');
    console.log('Connected to WebSocket');
};

ws.onclose = () => {
    connectionStatus.textContent = 'Disconnected';
    connectionStatus.classList.remove('connected');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);

    if (data.topic === 'home/security/camera/event') {
        const payload = data.payload;
        if (payload.event === 'intrusion_detected') {
            triggerLight();
            addLog(`🚨 ${payload.message}`, payload.timestamp);
        }
    } else if (data.topic === 'home/livingroom/environment') {
        const payload = data.payload;
        updateEnvironment(payload);
    }
};

function updateEnvironment(data) {
    document.getElementById('tempValue').textContent = `${data.temp} °C`;
    document.getElementById('humidValue').textContent = `${data.humidity} %`;
}

async function controlFan(action) {
    try {
        const response = await fetch(`/api/fan/${action}`, { method: 'POST' });
        const result = await response.json();
        addLog(`💨 Fan command sent: ${action.toUpperCase()}`, Date.now() / 1000);
    } catch (error) {
        console.error('Error controlling fan:', error);
    }
}

function triggerLight() {
    lightBulb.classList.add('on');
    lightStatusText.textContent = "INTRUDER!";
    lightStatusText.style.color = "#ff4757";
    
    // Reset timer if already running
    if (lightTimeout) clearTimeout(lightTimeout);

    // Turn off after 3 seconds
    lightTimeout = setTimeout(() => {
        lightBulb.classList.remove('on');
        lightStatusText.textContent = "SECURE";
        lightStatusText.style.color = "#e0e0e0";
    }, 3000);
}

function addLog(message, timestamp) {
    const li = document.createElement('li');
    const date = new Date(timestamp * 1000);
    const timeStr = date.toLocaleTimeString();
    
    li.innerHTML = `
        <span class="log-time">[${timeStr}]</span>
        <span>${message}</span>
    `;
    
    logList.prepend(li);
    
    // Keep only last 10 logs
    if (logList.children.length > 10) {
        logList.removeChild(logList.lastChild);
    }
}
