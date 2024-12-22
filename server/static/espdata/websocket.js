// Kết nối đến WebSocket server
const socket = new WebSocket('ws://127.0.0.1:8000/ws/espdata/');

// Khi kết nối WebSocket thành công
socket.onopen = function (event) {
    console.log("WebSocket connection established.");
};

// Khi nhận được dữ liệu từ server
socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    // Cập nhật Node 1
    if (data.node_id === 1) {
        document.querySelector('.temperature').innerHTML = `${data.temperature}<span>°C</span>`;
        document.querySelector('.humidity').innerHTML = `${data.humidity}<span>%RH</span>`;
        document.querySelector('.timestamp_box p').innerHTML = `Received at: ${data.timestamp}`;
    }

    // Cập nhật Node 2
    if (data.node_id === 2) {
        document.querySelector('.temperature').innerHTML = `${data.temperature}<span>°C</span>`;
        document.querySelector('.humidity').innerHTML = `${data.humidity}<span>%RH</span>`;
        document.querySelector('.timestamp_box p').innerHTML = `Received at: ${data.timestamp}`;
    }

    // Cập nhật Node 3
    if (data.node_id === 3) {
        document.querySelector('.temperature').innerHTML = `${data.temperature}<span>°C</span>`;
        document.querySelector('.humidity').innerHTML = `${data.humidity}<span>%RH</span>`;
        document.querySelector('.timestamp_box p').innerHTML = `Received at: ${data.timestamp}`;
    }
};

// Khi kết nối WebSocket bị lỗi
socket.onerror = function (error) {
    console.error("WebSocket error: ", error);
};

// Khi WebSocket bị đóng
socket.onclose = function (event) {
    console.log("WebSocket connection closed.");
};

