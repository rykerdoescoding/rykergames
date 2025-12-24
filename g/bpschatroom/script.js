// Ensure user is logged in
const username = localStorage.getItem('username');
if (!username) {
    window.location.href = "index.html";
}

// Connect to secure Socket.IO server (HTTPS)
const socket = io('https://chtsvcryker.giize.com:5000'); 

const chatBox = document.getElementById('chatBox');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

// Append message to chat box
function appendMessage(msg) {
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<b>${msg.user}:</b> ${msg.text}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message
function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    socket.emit('send_message', { user: username, text });
    messageInput.value = '';
}

sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Receive messages
socket.on('receive_message', appendMessage);

// Connection error handling
socket.on('connect_error', (err) => {
    console.error('Socket.IO connection error:', err);
    appendMessage({ user: 'System', text: 'Cannot connect to server. Check HTTPS.' });
});
