const username = localStorage.getItem('username');
if (!username) {
    window.location.href = "index.html";
}

const socket = io('http://chtsvcryker.giize.com:5000'); // Connect to server
const chatBox = document.getElementById('chatBox');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

// Send message
sendBtn.addEventListener('click', () => {
    const text = messageInput.value.trim();
    if (!text) return;
    socket.emit('send_message', { user: username, text });
    messageInput.value = '';
});

// Receive messages
socket.on('receive_message', (msg) => {
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<b>${msg.user}:</b> ${msg.text}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});
